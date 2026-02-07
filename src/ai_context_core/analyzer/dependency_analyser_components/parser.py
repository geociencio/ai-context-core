"""Logic for parsing common dependency files (requirements.txt, pyproject.toml, etc.)."""

import pathlib
from typing import Dict, List, Callable

DEPENDENCY_FILES = [
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
    "Pipfile",
    "setup.cfg",
    "environment.yml",
]

def parse_dependency_files(project_path: pathlib.Path, read_file_func: Callable) -> Dict[str, str]:
    """Read content from common dependency files."""
    files_content = {}
    for req_file in DEPENDENCY_FILES:
        path = project_path / req_file
        if path.exists():
            try:
                content = read_file_func(path)
                if content:
                    files_content[req_file] = content[:2000]
            except Exception:
                pass
    return files_content
