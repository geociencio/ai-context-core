"""Context freshness policy.

This module owns the high-level decision of whether rendered artifacts are
stale. The hashing and fingerprint primitives live in :mod:`verify`; keeping the
policy separate keeps both modules within the project complexity budget.
"""

import pathlib
from typing import Any, Dict

from ..analyzer.providers.config_loader import load_config
from ..analyzer.providers.fs_cache import compute_config_fingerprint
from .verify import (
    TRACKED_ARTIFACTS,
    _symbols_report,
    compute_content_hash,
    compute_render_fingerprint,
    read_recorded_meta,
)


def verify_context(project_path: pathlib.Path) -> Dict[str, Any]:
    """Verify that context artifacts are fresh relative to the current inputs.

    Args:
        project_path: Project root.

    Returns:
        A report with ``fresh``, ``reason``, ``recorded``, ``current``,
        ``missing``, ``symbols``, ``render_fingerprint``, ``config_fingerprint``
        and ``legacy``. ``legacy`` is ``True`` for artifacts rendered before the
        render fingerprint existed; those fall back to source-only comparison.
    """
    project_path = pathlib.Path(project_path).resolve()
    recorded_meta = read_recorded_meta(project_path)
    recorded = (recorded_meta or {}).get("content_hash")
    current = compute_content_hash(project_path)
    missing = [name for name in TRACKED_ARTIFACTS if not (project_path / name).exists()]
    symbols = _symbols_report(project_path, current, recorded_meta, missing)

    base_report = {
        "recorded": recorded,
        "current": current,
        "missing": missing,
        "symbols": symbols,
        "render_fingerprint": (recorded_meta or {}).get("render_fingerprint"),
        "config_fingerprint": None,
        "legacy": False,
    }

    if recorded is None:
        return {
            "fresh": False,
            "reason": "no recorded content hash (run 'ai-ctx context')",
            **base_report,
        }

    project_config = load_config(project_path)
    recorded_config_hash = (recorded_meta or {}).get("config_hash")
    current_config_hash = (
        compute_config_fingerprint(project_config) if recorded_config_hash else None
    )

    recorded_fingerprint = (recorded_meta or {}).get("render_fingerprint")
    legacy = not recorded_fingerprint
    current_fingerprint = None
    if recorded_fingerprint:
        fingerprint_config = project_config if recorded_config_hash else {}
        current_fingerprint = compute_render_fingerprint(
            project_path,
            fingerprint_config,
            current,
            include_md=(recorded_meta or {}).get("include_md"),
        )

    content_equal = recorded == current
    config_equal = not recorded_config_hash or recorded_config_hash == current_config_hash
    fingerprint_equal = legacy or recorded_fingerprint == current_fingerprint
    symbols_ok = symbols["fresh"] is not False

    fresh = content_equal and config_equal and fingerprint_equal and symbols_ok and not missing

    reason = ""
    if missing:
        reason = f"missing artifacts: {', '.join(missing)}"
    elif not content_equal:
        reason = "tracked sources changed since the last context render"
    elif not config_equal:
        reason = "configuration changed since the last context render"
    elif not fingerprint_equal:
        reason = "render inputs changed (embedded context docs or tool version)"
    elif not symbols_ok:
        reason = symbols["reason"]

    return {
        "fresh": fresh,
        "reason": reason,
        **base_report,
        "config_fingerprint": current_config_hash,
        "legacy": legacy,
    }
