"""Git analysis utilities for project evolution tracking.

This module provides tools to analyze git history, identify hotspots,
and calculate code churn.
"""

import pathlib
from typing import List, Dict, Any


from .git_analysis_components import (  # noqa: F401
    GitAnalyzer,
    GitRunner,
    GitParser,
)


def is_git_repo(path: pathlib.Path) -> bool:
    """Legacy wrapper for is_repo."""
    return GitAnalyzer(path).is_repo()


def get_git_hotspots(
    project_path: pathlib.Path, limit: int = 5, max_commits: int = 1000
) -> List[Dict[str, Any]]:
    """Legacy wrapper for get_hotspots."""
    return GitAnalyzer(project_path).get_hotspots(limit, max_commits)


def get_git_churn(project_path: pathlib.Path, days: int = 30) -> Dict[str, Any]:
    """Legacy wrapper for get_churn."""
    return GitAnalyzer(project_path).get_churn(days)


def analyze_git_evolution(project_path: pathlib.Path) -> Dict[str, Any]:
    """Performs a full evolution analysis using git history."""
    analyzer = GitAnalyzer(project_path)
    return {
        "hotspots": analyzer.get_hotspots(),
        "churn": analyzer.get_churn(),
        "is_repo": analyzer.is_repo(),
    }
