"""Logic for QGIS entry point detection and compliance auditing."""

import ast
from typing import Dict, Any
from .qgis_visitor import GenericQGISComplianceVisitor


def is_qgis_entry_point_node(node: ast.AST) -> bool:
    """Checks if an AST node is a QGIS classFactory entry point."""
    return (
        isinstance(node, ast.FunctionDef)
        and node.name == "classFactory"
        and any(arg.arg == "iface" for arg in node.args.args)
    )


def check_qgis_compliance(tree: ast.AST) -> Dict[str, Any]:
    """Checks for compliance with QGIS-specific coding standards."""
    no_i18n_lines = getattr(tree, "no_i18n_lines", frozenset())
    visitor = GenericQGISComplianceVisitor(no_i18n_lines=no_i18n_lines)
    visitor.visit(tree)
    return visitor.results
