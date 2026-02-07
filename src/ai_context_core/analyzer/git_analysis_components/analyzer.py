"""Git analysis orchestration logic."""

import pathlib
from typing import List, Dict, Any
from .runner import GitRunner
from .parser import GitParser

class GitAnalyzer:
    """Encapsulates git-based project analysis logic."""

    def __init__(self, project_path: pathlib.Path):
        """Initialize the git analyzer."""
        self.runner = GitRunner(project_path)
        self.parser = GitParser()
        self.path = project_path

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
        """Calculates code churn over the last N days."""
        if not self.is_repo():
            return {"available": False}
        since = f"--since='{days} days ago'"
        log = self.runner.run(["log", "--shortstat", "--no-merges", since, "--format="])
        return self.parser.parse_churn(log, days)
