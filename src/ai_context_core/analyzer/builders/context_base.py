"""Base classes for AI context builders."""

from typing import List

from .builders_base import BaseAnalysesBuilder


class BaseContextBuilder(BaseAnalysesBuilder):
    """Base class for building sections of the AI context document."""

    def build(self, lines: List[str]) -> None:
        """Builds the context section and appends to the lines list.

        Args:
            lines: List of markdown lines to append to.
        """
        raise NotImplementedError
