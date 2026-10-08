"""Base class for Builders in ai-context-core."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class BaseAnalysesBuilder:
    """Base for report section builders that consume a shared analyses mapping."""

    def __init__(self, analyses: Dict[str, Any]):
        """Initialize with analysis data.

        Args:
            analyses: Dictionary of analysis results.
        """
        self.analyses = analyses


class BaseBuilder(ABC):
    """Base class for builder pattern implementations.

    Enforces a common interface for building complex objects or results.
    """

    def __init__(self):
        """Initialize the builder."""
        self.errors: List[str] = []

    @abstractmethod
    def build(self) -> Any:
        """Builds and returns the result.

        Returns:
            The constructed object or result structure.
        """
        pass

    def _log_error(self, message: str):
        """Logs a builder error.

        Args:
            message: The error message.
        """
        self.errors.append(message)
        logger.warning(f"Builder Error: {message}")
