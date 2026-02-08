"""Design patterns detection module for ai-context-core.

Uses AST to identify common architectural patterns through a class-based detection system.
This module now acts as a facade for individual detectors located in `patterns_detectors`.
"""

import ast
from typing import Dict, Any


from .patterns_visitor import PatternsUnifiedVisitor


# Re-export individual detectors for backward compatibility (lazy)
def detect_singleton(tree):
    from .singleton import detect_singleton as _ds

    return _ds(tree)


def detect_factory(tree):
    from .factory import detect_factory as _df

    return _df(tree)


def detect_observer(tree):
    from .observer import detect_observer as _do

    return _do(tree)


def detect_strategy(tree):
    from .strategy import detect_strategy as _dst

    return _dst(tree)


def detect_decorator(tree):
    from .decorator import detect_decorator as _dd

    return _dd(tree)


from ..registry import register_detector  # noqa: E402

# Re-export individual detectors for backward compatibility


@register_detector("patterns")
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
