"""Git analysis utilities for project evolution tracking.

This module provides tools to analyze git history, identify hotspots,
and calculate code churn.
"""

import pathlib
from typing import Dict, Any

from .analyzer import GitAnalyzer


def analyze_git_evolution(project_path: pathlib.Path) -> Dict[str, Any]:
    """Performs a full evolution analysis using git history."""
    analyzer = GitAnalyzer(project_path)
    return {
        "hotspots": analyzer.get_hotspots(),
        "churn": analyzer.get_churn(),
        "is_repo": analyzer.is_repo(),
    }
