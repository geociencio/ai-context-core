"""Generic AST visitors for information extraction.

This module is a facade that re-exports functionality from ast_visitors_components.
"""

from .functions import FunctionVisitor, extract_functions
from .classes import ClassVisitor, extract_classes
from .docstrings import DocstringVisitor, check_docstrings
from .imports import ImportVisitor, extract_imports, detect_unused_imports

from ..registry import register_detector


@register_detector("unused_imports")
def detect_unused_imports_registered(tree):
    """Registered unused imports detector."""
    return detect_unused_imports(tree)


__all__ = [
    "FunctionVisitor",
    "extract_functions",
    "ClassVisitor",
    "extract_classes",
    "DocstringVisitor",
    "check_docstrings",
    "ImportVisitor",
    "extract_imports",
    "detect_unused_imports",
    "detect_unused_imports_registered",
]
