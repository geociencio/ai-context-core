"""Helpers to detect names re-exported via ``__all__``."""

import ast
from typing import Set


def _names_from_sequence(value: ast.AST) -> Set[str]:
    """Collect string literals from a ``__all__`` list/tuple expression.

    Args:
        value: The right-hand side of an ``__all__`` assignment.

    Returns:
        The set of exported names.
    """
    names: Set[str] = set()
    if isinstance(value, (ast.List, ast.Tuple)):
        for elt in value.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                names.add(elt.value)
    return names


def collect_exported_names(node: ast.AST) -> Set[str]:
    """Collect names exported by an ``__all__`` assignment statement.

    Supports both ``__all__ = [...]`` and ``__all__ += [...]``.

    Args:
        node: An AST statement node.

    Returns:
        The set of exported names declared by the statement (empty otherwise).
    """
    if isinstance(node, ast.Assign):
        targets = list(node.targets)
    elif isinstance(node, ast.AugAssign):
        targets = [node.target]
    else:
        return set()

    for target in targets:
        if isinstance(target, ast.Name) and target.id == "__all__":
            return _names_from_sequence(node.value)
    return set()
