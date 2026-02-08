"""Helper functions for i18n analysis."""

import ast
from typing import Dict, Any


def is_translatable_string(value: str, in_dict_key: bool = False) -> bool:
    """Determine if a string value should be counted as translatable.

    Args:
        value: String value to check
        in_dict_key: Whether this string is a dictionary key

    Returns:
        True if the string should be counted as translatable
    """
    if not isinstance(value, str):
        return False

    # Ignore dictionary keys
    if in_dict_key:
        return False

    # Ignore very short strings (likely not user-facing)
    if len(value) < 3:
        return False

    # Ignore paths and variable-like patterns
    if "/" in value or "\\" in value:
        return False

    # If it contains spaces, it's likely a sentence (unless it's a path, checked above)
    if " " in value:
        return True

    # If single word (no spaces):

    # Ignore snake_case and dotted.names
    if "_" in value or "." in value:
        return False

    # Ignore CamelCase or PascalCase (mixed case)
    if not value.islower() and not value.isupper():
        return False

    # Ignore UPPERCASE_CONSTANTS
    if value.isupper():
        return False

    # Allow simple lowercase words (e.g. "cancel", "ok")
    # although many might be technical keys, they are valid candidates.
    return True


def handle_i18n_call(node: ast.Call, results: Dict[str, Any]) -> None:
    """Processes a function call to count i18n usage."""
    try:
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            return

        if name == "tr":
            results["i18n_usage"]["tr"] += 1
        elif name == "translate":
            results["i18n_usage"]["translate"] += 1
    except Exception:
        pass
