"""Logic for loading ignore patterns from files or defaults."""

import pathlib
from typing import List, Optional

DEFAULT_IGNORE_PATTERNS = [
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    ".coverage",
    "build",
    "dist",
    "*.egg-info",
]


def load_ignore_patterns(
    project_path: pathlib.Path, extra_patterns: Optional[List[str]] = None
) -> List[str]:
    """Loads patterns from .analyzerignore or returns defaults."""
    patterns = []
    ignore_file = project_path / ".analyzerignore"

    if ignore_file.exists():
        try:
            with open(ignore_file, encoding="utf-8") as f:
                patterns = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
        except Exception:
            pass

    if not patterns:
        patterns = list(DEFAULT_IGNORE_PATTERNS)

    if extra_patterns:
        patterns.extend(extra_patterns)
    return patterns
