"""Git analysis utilities for project evolution tracking.

This module provides tools to analyze git history, identify hotspots,
and calculate code churn.
"""

import pathlib
from typing import Dict, Any, List, Optional

from .analyzer import GitAnalyzer


def analyze_git_evolution(
    project_path: pathlib.Path, exclusion_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Performs a full evolution analysis using git history.

    Args:
        project_path: Root directory of the analyzed project.
        exclusion_patterns: Extra patterns excluded from churn totals so the
            metric reflects analyzed code only.

    Returns:
        A dict with ``hotspots``, ``churn`` (code-scoped) and ``is_repo``.
    """
    analyzer = GitAnalyzer(project_path, exclusion_patterns)
    return {
        "hotspots": analyzer.get_hotspots(),
        "churn": analyzer.get_churn(),
        "is_repo": analyzer.is_repo(),
    }
