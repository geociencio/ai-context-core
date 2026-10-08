"""Base classes for report summarizers."""

from .builders_base import BaseAnalysesBuilder


class BaseSummarizer(BaseAnalysesBuilder):
    """Base class for building sections of the summary report."""

    def build(self) -> str:
        """Builds the summary section content.

        Returns:
            Formatted string content for the section.
        """
        raise NotImplementedError
