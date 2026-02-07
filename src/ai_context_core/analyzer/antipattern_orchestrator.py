"""Orchestrator for antipattern detection."""

import ast
from typing import List, Dict, Any
from . import antipatterns

def detect_all(tree: ast.AST) -> List[Dict[str, Any]]:
    """Run all antipattern detectors on the AST.

    Args:
        tree: The parsed AST of the module.

    Returns:
        List of detected anti-patterns with details.
    """
    return (
        antipatterns.detect_god_object(tree)
        + antipatterns.detect_spaghetti_code(tree)
        + antipatterns.detect_magic_numbers(tree)
        + antipatterns.detect_dead_code(tree)
    )
