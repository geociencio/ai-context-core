"""Base classes for entry point detection."""

import ast
from typing import Optional


class BaseEntryPointRule:
    """Base class for entry point detection rules."""

    def check(self, node: ast.AST) -> Optional[str]:
        """Checks if a node matches the rule and returns the type label.

        Args:
            node: The AST node to check.

        Returns:
            Type label (e.g., 'flask_app') if matched, else None.
        """
        raise NotImplementedError
