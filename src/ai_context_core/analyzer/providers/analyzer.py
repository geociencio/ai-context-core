"""Git analysis orchestration logic."""

import pathlib
from typing import List, Dict, Any, Optional
from .runner import GitRunner
from .parser import GitParser
from .ignore_filter import IgnoreFilter
from .git_churn import filter_churn


class GitAnalyzer:
    """Encapsulates git-based project analysis logic."""

    def __init__(self, project_path: pathlib.Path, exclusion_patterns: Optional[List[str]] = None):
        """Initialize the git analyzer.

        Args:
            project_path: Root directory of the analyzed project.
            exclusion_patterns: Extra patterns whose paths are excluded from
                churn totals, matching the analyzer's scan scope.
        """
        self.runner = GitRunner(project_path)
        self.parser = GitParser()
        self.path = project_path
        self.ignore = IgnoreFilter(project_path, list(exclusion_patterns or []))

    def is_repo(self) -> bool:
        """Checks if the path is inside a git repository."""
        out = self.runner.run(["rev-parse", "--is-inside-work-tree"], check=True)
        return out is not None

    def get_hotspots(self, limit: int = 5, max_commits: int = 1000) -> List[Dict[str, Any]]:
        """Identifies most frequently changed files."""
        if not self.is_repo():
            return []
        log = self.runner.run(["log", f"-n{max_commits}", "--format=", "--name-only"])
        return self.parser.parse_hotspots(log, limit)

    def get_churn(self, days: int = 30) -> Dict[str, Any]:
        """Calculates code churn over the last N days.

        The result is scoped to analyzed code (paths excluded by the analyzer
        are dropped); the original git-wide totals are kept under ``raw_*``.
        """
        if not self.is_repo():
            return {"available": False}
        log = self.runner.run(
            [
                "log",
                "--numstat",
                "--find-renames",
                "--no-merges",
                "--since",
                f"{days} days ago",
                "--format=",
            ]
        )
        churn = self.parser.parse_churn(log, days)
        if not churn.get("available"):
            return churn
        return filter_churn(churn, self._is_ignored)

    def _is_ignored(self, rel_path: str) -> bool:
        """Return whether a project-relative path is outside the analysis scope.

        Args:
            rel_path: Project-relative path from a git churn entry.

        Returns:
            True when the path is excluded by the analyzer's ignore patterns.
        """
        return self.ignore.is_ignored(self.path / rel_path)
