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
    visitor = GenericQGISComplianceVisitor()
    visitor.visit(tree)
    return visitor.results
