"""Git command execution logic."""

import subprocess
import pathlib
from typing import List, Optional


class GitRunner:
    """Handles execution of git commands."""

    def __init__(self, project_path: pathlib.Path):
        """Initialize the git runner."""
        self.path = project_path

    def run(self, args: List[str], check: bool = True) -> Optional[str]:
        """Runs a git command and returns its output."""
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=self.path,
                capture_output=True,
                text=True,
                check=check,
            )
            return res.stdout
        except Exception:
            return None
