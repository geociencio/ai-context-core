"""Handles loading and updating project context files."""

import pathlib
from typing import Dict, Any

from .store_components import (
    load_context_files,
    load_single_context_file,
    update_context_file,
)


class ContextStore:
    """Manages persistence of context data.

    Delegates file-specific loading and updating logic to specialized components.
    """

    FILE_LIST = ["project_context.json", "AI_CONTEXT.md", ".ai-context.yaml"]

    def __init__(self, project_path: pathlib.Path):
        """Initialize the store.

        Args:
            project_path: Path to the project root.
        """
        self.project_path = project_path

    def load_all(self) -> Dict[str, Any]:
        """Loads all relevant context files.

        Returns:
            Dictionary mapping filenames to their contents.
        """
        return load_context_files(self.project_path, self.FILE_LIST)

    def load_single(self, p: pathlib.Path) -> Any:
        """Loads a single context file based on extension.

        Args:
            p: Path to the file to load.

        Returns:
            Parsed content (dict, list) or raw text.
        """
        return load_single_context_file(p)

    def update(self, info: Dict[str, Any]):
        """Updates the context update file.

        Args:
            info: Dictionary of updates to apply.
        """
        update_context_file(self.project_path, info)
