"""Git output parsing logic for hotspots and churn."""

from typing import List, Dict, Any
from collections import Counter

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
    def parse_churn(shortstat_output: str, days: int) -> Dict[str, Any]:
        """Parses git shortstat output into churn metrics."""
        if not shortstat_output:
            return {"available": False}

        added, deleted, files = 0, 0, 0
        for line in shortstat_output.splitlines():
            if "file" in line and ("insertion" in line or "deletion" in line):
                parts = line.strip().split(",")
                files += int(parts[0].split()[0])
                for p in parts[1:]:
                    if "insertion" in p:
                        added += int(p.split()[0])
                    elif "deletion" in p:
                        deleted += int(p.split()[0])
        return {
            "available": True,
            "period_days": days,
            "added": added,
            "deleted": deleted,
            "total_churn": added + deleted,
            "files_changed": files,
        }
