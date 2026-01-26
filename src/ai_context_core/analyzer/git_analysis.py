"""Git analysis utilities for project evolution tracking.

Provides methods for identifying hotspots (frequently changed files)
and calculating the churn rate based on recent repository activity.
"""

import subprocess
import pathlib
from typing import List, Dict, Any


def is_git_repo(path: pathlib.Path) -> bool:
    """Checks if the given path is a Git repository.

    Args:
        path: Path to check.

    Returns:
        True if it's a git repo, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_git_hotspots(
    project_path: pathlib.Path, limit: int = 5
) -> List[Dict[str, Any]]:
    """Identifies files with the most changes in the repository history.

    Args:
        project_path: Path to the project root.
        limit: Maximum number of hotspots to return.

    Returns:
        A list of dictionaries with 'path' and 'commits' count.
    """
    if not is_git_repo(project_path):
        return []

    try:
        # Use git log to get the number of times each file has been modified
        result = subprocess.run(
            ["git", "log", "--format=", "--name-only"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        files = [
            f for f in result.stdout.splitlines() if f.strip() and f.endswith(".py")
        ]
        from collections import Counter

        counts = Counter(files).most_common(limit)

        return [{"path": path, "commits": count} for path, count in counts]
    except Exception:
        return []


def get_git_churn(project_path: pathlib.Path, days: int = 30) -> Dict[str, Any]:
    """Calculates the code churn (lines added/deleted) in the last N days.

    Args:
        project_path: Path to the project root.
        days: Number of days to look back.

    Returns:
        A dictionary with 'added', 'deleted', and 'total' churn.
    """
    if not is_git_repo(project_path):
        return {"available": False}

    try:
        # Get shortstat for the last N days
        since = f"--since='{days} days ago'"
        result = subprocess.run(
            ["git", "log", "--shortstat", "--no-merges", since, "--format="],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True,
        )

        lines = result.stdout.splitlines()
        added = 0
        deleted = 0
        files_changed = 0

        for line in lines:
            if "file" in line and ("insertion" in line or "deletion" in line):
                parts = line.strip().split(",")
                files_changed += int(parts[0].split()[0])
                for part in parts[1:]:
                    if "insertion" in part:
                        added += int(part.split()[0])
                    elif "deletion" in part:
                        deleted += int(part.split()[0])

        return {
            "available": True,
            "period_days": days,
            "added": added,
            "deleted": deleted,
            "total_churn": added + deleted,
            "files_changed": files_changed,
        }
    except Exception:
        return {"available": False}
