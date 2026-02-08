"""Base class for AST visitors in ai-context-core."""

import ast
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseVisitor(ast.NodeVisitor):
    """Base visitor class providing common functionality for AST traversal.

    Features:
    - Standardized error logging in visit methods (via wrapper or convention)
    - Common state management for errors and results
    """

    def __init__(self):
        """Initialize the base visitor."""
        self.errors: List[Dict[str, Any]] = []
        self._current_file: Optional[str] = None

    def visit(self, node: ast.AST):
        """Override visit to provide safety or logging if needed.

        Currently delegates to super().visit, but serves as an extension point.
        """
        try:
            super().visit(node)
        except Exception as e:
            self._log_error(
                f"Error visiting node {type(node).__name__}: {str(e)}", node
            )

    def _log_error(self, message: str, node: Optional[ast.AST] = None):
        """Log an error and append it to the errors list.

        Args:
            message: The error message.
            node: The AST node associated with the error (optional).

        """
        lineno = getattr(node, "lineno", "N/A") if node else "N/A"
        error_entry = {"message": message, "line": lineno, "file": self._current_file}
        self.errors.append(error_entry)
        logger.debug(f"Visitor Error [{self._current_file}:{lineno}]: {message}")
