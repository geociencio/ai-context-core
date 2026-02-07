"""Base classes for AI context builders."""

from typing import Dict, Any, List

class BaseContextBuilder:
    """Base class for building sections of the AI context document."""

    def __init__(self, analyses: Dict[str, Any]):
        """Initialize with analysis data.

        Args:
            analyses: Dictionary of analysis results.
        """
        self.analyses = analyses

    def build(self, lines: List[str]) -> None:
        """Builds the context section and appends to the lines list.

        Args:
            lines: List of markdown lines to append to.
        """
        raise NotImplementedError
