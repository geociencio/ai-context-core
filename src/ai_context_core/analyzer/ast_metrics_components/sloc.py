"""SLOC (Source Lines of Code) calculation logic."""

import ast
import io
import tokenize

from .sloc_helpers import get_docstring_ranges

def calculate_sloc(tree: ast.AST, content: str) -> int:
    """Calculates Source Lines of Code (SLOC).

    Excludes blank lines, comments, and docstrings.
    
    Args:
        tree: The AST of the module.
        content: The raw source code.

    Returns:
        Number of logical source lines.
    """
    doc_ranges = get_docstring_ranges(tree)
    lines_with_code = set()

    try:
        tokens = tokenize.generate_tokens(io.StringIO(content).readline)
        for tok in tokens:
            if _should_skip_token(tok, doc_ranges):
                continue
            
            for line_idx in range(tok.start[0], tok.end[0] + 1):
                lines_with_code.add(line_idx)
        return len(lines_with_code)
    except Exception:
        return _fallback_sloc(content)


def _should_skip_token(tok: tokenize.TokenInfo, doc_ranges: List[Tuple[int, int]]) -> bool:
    """Checks if a token should be excluded from SLOC count.

    Args:
        tok: The token to check.
        doc_ranges: List of line ranges containing docstrings.

    Returns:
        True if the token should be ignored.
    """
    ignored = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, 
               tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER)
    if tok.type in ignored:
        return True
    
    return any(start <= tok.start[0] <= end for start, end in doc_ranges)


def _fallback_sloc(content: str) -> int:
    """Simple SLOC calculation as a fallback when tokenization fails."""
    lines = [line.strip() for line in content.splitlines()]
    return len([line for line in lines if line and not line.startswith("#")])

from typing import List, Tuple, Optional
