"""Base interface for issue checkers."""

from typing import List, Dict, Any


class BaseChecker:
    """Abstract base class for all issue checkers."""

    def check(self, module_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run the check on the module.

        Args:
            module_info: Dictionary containing module analysis data

        Returns:
            List of detected issues
        """
        raise NotImplementedError

    def get_category(self) -> str:
        """Return the category of issues this checker detects."""
        raise NotImplementedError

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize checker with configuration."""
        self.config = config or {}

    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for this checker."""
        return {}
