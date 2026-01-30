"""AST utilities for Python code analysis.

This module is now a deprecated facade. Please import from the specific submodules:
- ai_context_core.analyzer.ast_visitors
- ai_context_core.analyzer.ast_metrics
- ai_context_core.analyzer.ast_entry_points
- ai_context_core.analyzer.ast_qgis
"""

import ast
from .ast_visitors import (
    extract_functions,
    extract_classes,
    check_docstrings,
    extract_imports,
    detect_unused_imports,
)
from .ast_metrics import (
    calculate_complexity,
    calculate_halstead_metrics,
    calculate_type_hint_coverage,
)
from .ast_entry_points import is_entry_point
from .ast_qgis import check_qgis_compliance

# Re-export symbols for backward compatibility


def extract_base_name(node: ast.AST) -> str:
    """Helper to extract the name of a base class from a node.

    Args:
        node: The AST node to extract the name from

    Returns:
        The extracted name or 'Unknown' if extraction fails
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Call):
        return extract_base_name(node.func)
    return "Unknown"
