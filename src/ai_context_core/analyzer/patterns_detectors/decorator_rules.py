"""Specialized rules for detecting Decorator pattern indicators."""

import ast
from typing import Optional


class DecoratorRules:
    """Encapsulates patterns for Decorator detection."""

    @classmethod
    def find_inner_function(cls, node: ast.AST) -> Optional[ast.AST]:
        """Finds the first inner function definition.

        Args:
            node: Node to search within.

        Returns:
            Inner function node or None.
        """
        return next(
            (
                i
                for i in getattr(node, "body", [])
                if isinstance(i, (ast.FunctionDef, ast.AsyncFunctionDef))
            ),
            None,
        )

    @classmethod
    def returns_inner(cls, node: ast.AST, inner_name: str) -> bool:
        """Checks if the node returns the named inner function.

        Args:
            node: Parent function node.
            inner_name: Name of the inner function.

        Returns:
            True if it returns the inner function.
        """
        for i in getattr(node, "body", []):
            if (
                isinstance(i, ast.Return)
                and isinstance(i.value, ast.Name)
                and i.value.id == inner_name
            ):
                return True
        return False

    @classmethod
    def has_wraps(cls, node: ast.AST) -> bool:
        """Checks for @functools.wraps usage.

        Args:
            node: Function node to check decorators list.

        Returns:
            True if wraps is found.
        """
        for d in getattr(node, "decorator_list", []):
            if isinstance(d, ast.Call):
                name = getattr(d.func, "attr", getattr(d.func, "id", ""))
                if name == "wraps":
                    return True
        return False

    @classmethod
    def is_class_decorator(cls, node: ast.ClassDef) -> bool:
        """Checks if class implements decorator interface."""
        names = {i.name for i in node.body if isinstance(i, ast.FunctionDef)}
        return "__init__" in names and "__call__" in names
