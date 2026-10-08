"""Static analysis tools for identifying security risks and optimization opportunities."""

import ast
from typing import List, Dict, Any

from ..providers.secrets_scanner import find_secrets  # noqa: F401
from .optimizations import find_optimizations  # noqa: F401
from ..registry import register_detector


@register_detector("ast_security")
def detect(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects security issues in the AST.

    Args:
        tree: The AST to analyze.

    Returns:
        List of detected security issues.
    """
    from .ast_security import detect_ast_security_issues as _detect_ast_security

    return _detect_ast_security(tree)
