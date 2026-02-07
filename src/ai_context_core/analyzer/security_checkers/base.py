"""Base classes for security issue detection."""

import ast
from typing import List, Dict, Any


class BaseSecurityChecker:
    """Base class for security detection rules."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the checker with configuration.

        Args:
            config: Configuration dictionary.
        """
        self.config = config or {}

    def check(self, node: ast.AST, issues: List[Dict[str, Any]]) -> None:
        """Analyzes a node and adds detected issues to the list.

        Args:
            node: The AST node to analyze.
            issues: The list to append detected issues to.
        """
        raise NotImplementedError
