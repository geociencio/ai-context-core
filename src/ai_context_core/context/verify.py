"""Context staleness verification.

Each rendered artifact records a ``content_hash`` of the analyzed Python inputs
(relative path + file hash) in its ``_meta`` block. ``verify`` recomputes that
hash and reports drift when a tracked file has changed or an artifact is missing.
"""

import hashlib
import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

from ..analyzer.providers import fs_utils

logger = logging.getLogger(__name__)

AI_CONTEXT = "AI_CONTEXT.md"
PROJECT_CONTEXT = "project_context.json"
MANIFEST = "context_manifest.json"
SYMBOLS = "symbols.json"
TRACKED_ARTIFACTS = (AI_CONTEXT, PROJECT_CONTEXT, MANIFEST)

HASH_PREFIX = "sha256:"


def compute_content_hash(
    project_path: pathlib.Path, exclusion_patterns: Optional[List[str]] = None
) -> str:
    """Hash the analyzed Python inputs (relative path + file content hash).

    Args:
        project_path: Project root.
        exclusion_patterns: Extra ignore patterns; resolved from the project when
            omitted.

    Returns:
        A ``sha256:<hex>`` string, stable across runs for unchanged inputs.
    """
    project_path = pathlib.Path(project_path).resolve()
    if exclusion_patterns is None:
        exclusion_patterns = fs_utils.load_exclusion_patterns(project_path, None)

    scan = fs_utils.scan_project(project_path, exclusion_patterns)
    return hash_files(project_path, scan.python_files)


def hash_files(project_path: pathlib.Path, files: List[pathlib.Path]) -> str:
    """Hash a pre-scanned list of files (relative path + content hash).

    Lets callers that already scanned the project avoid a redundant walk.

    Args:
        project_path: Project root.
        files: Files to include in the hash.

    Returns:
        A ``sha256:<hex>`` string.
    """
    project_path = pathlib.Path(project_path).resolve()
    entries: List[List[str]] = []
    for file_path in files:
        try:
            rel = str(pathlib.Path(file_path).relative_to(project_path))
            entries.append([rel, _hash_file(file_path)])
        except OSError as e:  # pragma: no cover - unreadable file
            logger.warning("Skipping %s during hashing: %s", file_path, e)
    entries.sort()

    payload = json.dumps(entries, separators=(",", ":")).encode("utf-8")
    return HASH_PREFIX + hashlib.sha256(payload).hexdigest()


def _hash_file(path: pathlib.Path) -> str:
    """Hash file bytes directly (bypasses the process-global read cache)."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_recorded_hash(project_path: pathlib.Path) -> Optional[str]:
    """Read the recorded ``content_hash`` from the manifest or context JSON."""
    project_path = pathlib.Path(project_path)
    for name in (MANIFEST, PROJECT_CONTEXT):
        data = _read_json(project_path / name)
        recorded = (data or {}).get("_meta", {}).get("content_hash")
        if recorded:
            return recorded
    return None


def verify_context(project_path: pathlib.Path) -> Dict[str, Any]:
    """Verify that context artifacts are fresh relative to the current sources.

    Args:
        project_path: Project root.

    Returns:
        A report with ``fresh``, ``recorded``, ``current`` and ``missing``.
    """
    project_path = pathlib.Path(project_path).resolve()
    recorded = read_recorded_hash(project_path)
    current = compute_content_hash(project_path)
    missing = [name for name in TRACKED_ARTIFACTS if not (project_path / name).exists()]

    if recorded is None:
        return {
            "fresh": False,
            "reason": "no recorded content hash (run 'ai-ctx context')",
            "recorded": None,
            "current": current,
            "missing": missing,
        }

    fresh = recorded == current and not missing
    reason = ""
    if missing:
        reason = f"missing artifacts: {', '.join(missing)}"
    elif recorded != current:
        reason = "tracked sources changed since the last context render"

    return {
        "fresh": fresh,
        "reason": reason,
        "recorded": recorded,
        "current": current,
        "missing": missing,
    }


def _read_json(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file, returning ``None`` on absence or error."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        logger.warning("Could not read %s: %s", path, e)
        return None
