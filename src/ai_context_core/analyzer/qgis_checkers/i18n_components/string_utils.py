"""Utilities for identifying translatable strings."""

import re

# Naming patterns for technical identifiers
# snake_case: starts with alpha, then alpha/num/underscore
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
# camelCase: starts with lower, then mixed case
CAMEL_CASE = re.compile(r"^[a-z][a-z0-9]*([A-Z][a-z0-9]*)+$")
# PascalCase: starts with upper, then mixed case
PASCAL_CASE = re.compile(r"^[A-Z][a-z0-9]*([A-Z][a-z0-9]*)+$")
# UPPER_CASE: all upper with underscores
UPPER_CASE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def is_translatable_string(text: str) -> bool:
    """Checks if a string is likely translatable (not a path, URL, or placeholder).

    Args:
        text: The string to check.

    Returns:
        True if the string is likely human-readable text.
    """
    val = text.strip()
    if not val or len(val) <= 1:
        return False

    # Basic exclusions (always apply)
    is_path = val.startswith(("/", "./", "../")) or "\\" in val
    is_url = any(val.startswith(p) for p in ("http://", "https://", "ftp://"))
    is_placeholder = val.replace("{}", "").replace("%s", "").strip() == ""

    if is_path or is_url or is_placeholder:
        return False

    # Filters based on spaces (technical identifiers usually don't have spaces)
    if " " in val:
        return True

    # No spaces: check for technical naming patterns
    # If it matches a pattern and has no spaces, it's likely a technical identifier
    if (
        SNAKE_CASE.match(val)
        or CAMEL_CASE.match(val)
        or PASCAL_CASE.match(val)
        or UPPER_CASE.match(val)
    ):
        return False

    # Special case: dotted identifiers (e.g., "data.value")
    if "." in val and all(part.isidentifier() for part in val.split(".") if part):
        return False

    return any(c in val for c in ".,!?;")
