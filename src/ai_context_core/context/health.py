"""Context health: freshness, token size, symbol coverage and provenance.

There is **no quality gate** in the context-only contract; staleness is the only
condition that makes ``health`` fail.
"""

import json
import pathlib
from typing import Any, Dict, Optional

from .symbol_index import SYMBOLS_FILE
from .verify import MANIFEST, verify_context


def compute_health(project_path: pathlib.Path) -> Dict[str, Any]:
    """Compute a context-health report.

    Args:
        project_path: Project root.

    Returns:
        A report with freshness, token usage, symbol coverage and provenance.
    """
    project_path = pathlib.Path(project_path).resolve()
    report = verify_context(project_path)
    manifest = _read_json(project_path / MANIFEST) or {}
    symbols = _read_json(project_path / SYMBOLS_FILE) or {}

    return {
        "fresh": report["fresh"],
        "reason": report["reason"],
        "missing": report["missing"],
        "tokens": {
            "total": manifest.get("total_tokens"),
            "budget": manifest.get("budget"),
            "truncated": manifest.get("truncated", False),
        },
        "symbols": {
            "definitions": len(symbols.get("symbols", [])),
            "references": len(symbols.get("references", [])),
        },
        "provenance": manifest.get("_meta", {}),
    }


def _read_json(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file, returning ``None`` on absence or error."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
