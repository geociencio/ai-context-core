"""Severity helpers for security issue aggregation."""

from typing import Any, Dict, Iterable, List

_SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def max_severity(issues: Iterable[Dict[str, Any]]) -> str:
    """Return the highest severity label present in ``issues``.

    Args:
        issues: Security issue dictionaries carrying an optional ``severity``.

    Returns:
        The most severe label found (``low``, ``medium``, ``high`` or
        ``critical``), defaulting to ``low`` when no issue is present.
    """
    items: List[Dict[str, Any]] = list(issues)
    if not items:
        return "low"
    return max(
        (str(i.get("severity", "low")).lower() for i in items),
        key=lambda s: _SEVERITY_RANK.get(s, 0),
    )
