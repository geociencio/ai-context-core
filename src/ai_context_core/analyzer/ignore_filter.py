"""Logic for filtering and ignoring files based on patterns during project scan."""

import pathlib

import fnmatch
import re
from typing import List, Optional


from .ignore_components import load_ignore_patterns, compile_ignore_patterns

class IgnoreFilter:
    """Handles logic for filtering files and directories based on exclusion patterns.
    
    Delegates pattern loading and regex compilation to specialized internal components.
    """

    def __init__(
        self, project_path: pathlib.Path, extra_patterns: Optional[List[str]] = None
    ):
        """Initialize the filter.

        Args:
            project_path: Path to the project root.
            extra_patterns: Optional list of additional patterns to ignore.
        """
        self.project_path = project_path
        self.patterns = load_ignore_patterns(project_path, extra_patterns)
        self.regex = compile_ignore_patterns(self.patterns)

    def is_ignored(self, path: pathlib.Path) -> bool:
        """Checks if a path or any of its parents should be ignored.

        Args:
            path: Path to check.

        Returns:
            True if the path should be excluded from analysis.
        """
        if not self.regex:
            return False

        try:
            rel_path = path.relative_to(self.project_path)
        except ValueError:
            rel_path = path

        # 1. Check if any parent directory is ignored
        for part in rel_path.parts:
            if self.regex.match(part):
                return True

        # 2. Check the full relative path string (e.g. 'docs/*.html')
        rel_path_str = str(rel_path).replace("\\", "/")
        return bool(self.regex.match(rel_path_str))
