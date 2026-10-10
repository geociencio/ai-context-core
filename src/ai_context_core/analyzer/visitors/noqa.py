"""``# noqa`` opt-out detection shared by AST-based checkers.

AST nodes do not retain comments, so honoring a ``# noqa`` directive requires
mapping comments back to their lines with :mod:`tokenize` (the same technique the
SLOC counter uses).
"""

import io
import re
import tokenize
from typing import Set

_NOQA_RE = re.compile(r"#\s*noqa(?:\s*:\s*(?P<codes>[A-Za-z0-9,\s]+))?", re.IGNORECASE)


def _suppresses_imports(comment: str) -> bool:
    """Whether a comment is a bare ``# noqa`` or lists the ``F401`` code."""
    match = _NOQA_RE.search(comment)
    if not match:
        return False
    codes = match.group("codes")
    if codes is None:
        return True
    return "F401" in {c.strip().upper() for c in re.split(r"[,\s]+", codes) if c.strip()}


def find_noqa_lines(content: str) -> Set[int]:
    """Return the 1-based line numbers carrying a relevant ``# noqa`` directive.

    A bare ``# noqa`` suppresses every finding on that line; ``# noqa: F401``
    (or a code list that includes ``F401``) suppresses unused-import findings.

    Args:
        content: Source code of the module.

    Returns:
        Set of line numbers carrying a relevant ``# noqa`` comment. Malformed
        input yields an empty set.
    """
    try:
        tokens = tokenize.generate_tokens(io.StringIO(content).readline)
        return {
            tok.start[0]
            for tok in tokens
            if tok.type == tokenize.COMMENT and _suppresses_imports(tok.string)
        }
    except (tokenize.TokenError, IndentationError, SyntaxError):  # pragma: no cover
        return set()
