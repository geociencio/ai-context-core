"""Design patterns detection module for ai-context-core.

Uses AST to identify common architectural patterns through a class-based detection system.
This module now acts as a facade for individual detectors located in `patterns_detectors`.
"""

import ast
from typing import Dict, Any


from .patterns_components import PatternsUnifiedVisitor

# Re-export individual detectors for backward compatibility


def detect_patterns(tree: ast.AST) -> Dict[str, Any]:
    """Analyzes an AST to detect common design patterns using a unified visitor.

    Args:
        tree: The AST tree to analyze.

    Returns:
        Dictionary of detected patterns and their occurrences.
    """
    visitor = PatternsUnifiedVisitor()
    visitor.visit(tree)
    return visitor.results
