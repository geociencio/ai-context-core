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
    """Checks for compliance with QGIS-specific coding standards.

    Reads optional ``ignored_functions`` / ``ui_functions`` overrides from the
    ``i18n_config`` attribute attached to the tree by the analysis worker.
    """
    no_i18n_lines = getattr(tree, "no_i18n_lines", frozenset())
    i18n_config = getattr(tree, "i18n_config", None) or {}
    visitor = GenericQGISComplianceVisitor(
        no_i18n_lines=no_i18n_lines,
        ignored_functions=i18n_config.get("ignored_functions"),
        ui_functions=i18n_config.get("ui_functions"),
    )
    visitor.visit(tree)
    return visitor.results
