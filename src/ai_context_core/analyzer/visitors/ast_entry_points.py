"""Entry point detection (context).

Context-only (v5.0.0): detection is limited to the standard ``__main__`` guard.
Framework-specific (Flask/FastAPI/Django/QGIS) entry-point heuristics moved to
``qgis-plugin-analyzer`` (supersedes ADR-0004).
"""

import ast
from typing import Any, Dict


class EntryPointVisitor(ast.NodeVisitor):
    """Detect whether a module is an entry point via the ``__main__`` guard."""

    def __init__(self):
        """Initialize the entry point visitor."""
        self.result: Dict[str, Any] = {"is_entry_point": False, "type": None}

    def visit_If(self, node: ast.If):
        """Check for ``if __name__ == "__main__":`` guards."""
        if not self.result["is_entry_point"] and self._is_main_guard(node):
            self.result = {"is_entry_point": True, "type": "main_guard"}
        self.generic_visit(node)

    def _is_main_guard(self, node: ast.If) -> bool:
        """Heuristic for 'if __name__ == "__main__":'."""
        try:
            return (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                and any(
                    isinstance(c, ast.Constant) and c.value == "__main__"
                    for c in node.test.comparators
                )
            )
        except Exception:
            return False


def is_entry_point(tree: ast.AST) -> Dict[str, Any]:
    """Analyze a module to determine if it acts as an entry point.

    Args:
        tree: The AST to analyze.

    Returns:
        Dictionary with ``is_entry_point`` (bool) and ``type`` (str).
    """
    visitor = EntryPointVisitor()
    visitor.visit(tree)
    return visitor.result


def has_main_guard(tree: ast.AST) -> bool:
    """Return True when the module contains the standard ``__main__`` guard.

    Args:
        tree: The AST to analyze.

    Returns:
        True if a main guard is found.
    """
    result = is_entry_point(tree)
    return result["is_entry_point"] and result["type"] == "main_guard"
