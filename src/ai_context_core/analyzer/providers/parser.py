"""Git output parsing logic for hotspots and churn."""

from typing import List, Dict, Any
from collections import Counter


def _rename_new_path(path: str) -> str:
    """Extract the new path from a git rename marker (``{old => new}suffix``)."""
    if "=>" not in path:
        return path
    return path.split("=>", 1)[1].replace("}", "").strip()


class GitParser:
    """Parses git command outputs into structured data."""

    @staticmethod
    def parse_hotspots(log_output: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Parses git log output into a list of hotspots."""
        if not log_output:
            return []
        files = [f for f in log_output.splitlines() if f.strip() and f.endswith(".py")]
        return [{"path": p, "commits": c} for p, c in Counter(files).most_common(limit)]

    @staticmethod
    def parse_churn(numstat_output: str, days: int) -> Dict[str, Any]:
        """Parses git numstat output into per-file churn metrics.

        Args:
            numstat_output: Output of ``git log --numstat --find-renames``.
            days: The churn period in days.

        Returns:
            A dict with total added/deleted/churn plus a ``per_file`` mapping
            of ``{path: {"added": int, "deleted": int}}``.
        """
        if not numstat_output:
            return {"available": False}

        per_file: Dict[str, Dict[str, int]] = {}
        for line in numstat_output.splitlines():
            parts = line.split("\t", 2)
            if len(parts) < 3:
                continue
            added_raw, deleted_raw, path = parts[0], parts[1], parts[2].strip()
            path = _rename_new_path(path)
            if added_raw == "-" or deleted_raw == "-":
                continue
            try:
                added = int(added_raw)
                deleted = int(deleted_raw)
            except ValueError:
                continue
            counts = per_file.setdefault(path, {"added": 0, "deleted": 0})
            counts["added"] += added
            counts["deleted"] += deleted

        added = sum(c["added"] for c in per_file.values())
        deleted = sum(c["deleted"] for c in per_file.values())
        return {
            "available": True,
            "period_days": days,
            "added": added,
            "deleted": deleted,
            "total_churn": added + deleted,
            "files_changed": len(per_file),
            "per_file": per_file,
        }
