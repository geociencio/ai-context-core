"""Helper functions for i18n analysis."""

import ast
import io
import tokenize
from typing import Dict, Any, FrozenSet


def _dominated_by_punctuation(value: str) -> bool:
    """Return True when punctuation outnumbers alphabetic characters."""
    alpha = sum(c.isalpha() for c in value)
    punct = sum(not c.isalnum() and not c.isspace() for c in value)
    return punct > alpha


def is_translatable_string(value: str) -> bool:
    """Determine if a string value should be counted as translatable.

    Dictionary-key context is tracked externally by the caller
    (see ``GenericQGISComplianceVisitor.visit_Dict``).

    Args:
        value: String value to check

    Returns:
        True if the string should be counted as translatable
    """
    if not isinstance(value, str):
        return False

    # Ignore very short strings (likely not user-facing)
    if len(value) < 3:
        return False

    # Ignore paths and variable-like patterns
    if "/" in value or "\\" in value:
        return False

    # Ignore strings dominated by punctuation (technical tokens)
    if _dominated_by_punctuation(value):
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


def find_no_i18n_lines(source: str) -> FrozenSet[int]:
    """Return line numbers annotated with a `# no-i18n` opt-out comment."""
    lines = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT and "no-i18n" in tok.string:
                lines.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError, ValueError):
        pass
    return frozenset(lines)


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
