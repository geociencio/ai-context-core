"""Base classes for QGIS compliance detection."""

import ast
from typing import Dict, Any


class BaseQGISChecker:
    """Base class for QGIS compliance detection rules."""

    def __init__(self, results: Dict[str, Any]):
        """Initialize the checker with results dictionary to update.

        Args:
            results: Shared results dictionary.
        """
        self.results = results

    def visit(self, node: ast.AST) -> None:
        """Entry point for checking a node."""
        raise NotImplementedError

    def generic_visit_with_docstring_skip(
        self, visitor: ast.NodeVisitor, node: ast.AST
    ):
        """Helper to visit children while skipping the docstring of the current node."""
        docstring = ast.get_docstring(node, clean=False)
        body = getattr(node, "body", [])
        start_idx = (
            1 if docstring is not None and body and isinstance(body[0], ast.Expr) else 0
        )

        for child in body[start_idx:]:
            visitor.visit(child)

        self._visit_extra_parts(visitor, node)

    def _visit_extra_parts(self, visitor: ast.NodeVisitor, node: ast.AST):
        """Visits decorators and other non-body parts of functions/classes."""
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return

        for decorator in node.decorator_list:
            visitor.visit(decorator)

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in node.args.args:
                visitor.visit(arg)
            if node.returns:
                visitor.visit(node.returns)
        elif isinstance(node, ast.ClassDef):
            for base in node.bases:
                visitor.visit(base)
