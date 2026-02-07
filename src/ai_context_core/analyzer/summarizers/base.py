"""Base classes for report summarizers."""

from typing import Dict, Any

class BaseSummarizer:
    """Base class for building sections of the summary report."""

    def __init__(self, analyses: Dict[str, Any]):
        """Initialize with analysis data.

        Args:
            analyses: Dictionary of analysis results.
        """
        self.analyses = analyses

    def build(self) -> str:
        """Builds the summary section content.

        Returns:
            Formatted string content for the section.
        """
        raise NotImplementedError
