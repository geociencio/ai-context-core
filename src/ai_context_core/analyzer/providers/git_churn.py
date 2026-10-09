"""Churn filtering: scope git churn to the files the analyzer actually reads."""

from typing import Any, Callable, Dict


def filter_churn(churn: Dict[str, Any], should_ignore: Callable[[str], bool]) -> Dict[str, Any]:
    """Restrict a churn result to non-ignored files.

    The totals are recomputed over the kept files, and the original git-wide
    totals are preserved under ``raw_*`` keys for context.

    Args:
        churn: A churn dict as returned by ``GitParser.parse_churn``.
        should_ignore: Predicate deciding whether a project-relative path is
            excluded from analysis (e.g. documentation or build artifacts).

    Returns:
        A new churn dict scoped to analyzed code, augmented with ``raw_added``,
        ``raw_deleted`` and ``raw_total_churn``.
    """
    per_file = {
        path: counts
        for path, counts in churn.get("per_file", {}).items()
        if not should_ignore(path)
    }
    added = sum(c["added"] for c in per_file.values())
    deleted = sum(c["deleted"] for c in per_file.values())
    raw_added = churn.get("added", 0)
    raw_deleted = churn.get("deleted", 0)
    return {
        **churn,
        "added": added,
        "deleted": deleted,
        "total_churn": added + deleted,
        "files_changed": len(per_file),
        "per_file": per_file,
        "raw_added": raw_added,
        "raw_deleted": raw_deleted,
        "raw_total_churn": raw_added + raw_deleted,
    }
