"""Generic AST visitors for information extraction.

This module is a facade that re-exports functionality from ast_visitors_components.
"""

from .ast_visitors_components import (
    FunctionVisitor,
    extract_functions,
    ClassVisitor,
    extract_classes,
    DocstringVisitor,
    check_docstrings,
    ImportVisitor,
    extract_imports,
    detect_unused_imports,
)

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
]
