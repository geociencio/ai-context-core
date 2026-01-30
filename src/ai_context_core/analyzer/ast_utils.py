"""AST utilities for Python code analysis.

This module is now a deprecated facade. Please import from the specific submodules:
- ai_context_core.analyzer.ast_visitors
- ai_context_core.analyzer.ast_metrics
- ai_context_core.analyzer.ast_entry_points
- ai_context_core.analyzer.ast_qgis
"""

import ast

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
