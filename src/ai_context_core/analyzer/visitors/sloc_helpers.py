"""Helpers for identifying docstring ranges during SLOC calculation."""

import ast
from typing import List, Tuple, Optional


def get_docstring_ranges(tree: ast.AST) -> List[Tuple[int, int]]:
    """Identifies line ranges for all docstrings in the AST."""
    ranges = []
    for node in ast.walk(tree):
        if not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue

        doc_node = _find_docstring_node(node)
        if doc_node:
            ranges.append((doc_node.lineno, doc_node.end_lineno))
    return ranges


def _find_docstring_node(node: ast.AST) -> Optional[ast.AST]:
    """Retrieves the literal node containing a docstring, if any."""
    if not (node.body and isinstance(node.body[0], ast.Expr)):
        return None

    expr = node.body[0].value
    # Support both old and new AST styles
    if isinstance(expr, (ast.Constant, getattr(ast, "Str", ast.Constant))):
        if hasattr(node.body[0], "lineno") and hasattr(node.body[0], "end_lineno"):
            return node.body[0]
    return None
