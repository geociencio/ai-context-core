"""Detects GDAL and Qt import styles and versions."""

import ast
from .base import BaseQGISChecker

from .import_components import handle_qgis_import, handle_qgis_import_from


class ImportStyleChecker(BaseQGISChecker):
    """Checks for GDAL import styles and PyQt vs PySide usage.

    Delegates node-specific handling to internal components.
    """

    def visit(self, node: ast.AST) -> None:
        """Visits nodes to detect GDAL and Qt import patterns."""
        if isinstance(node, ast.Import):
            handle_qgis_import(node, self.results)
        elif isinstance(node, ast.ImportFrom):
            handle_qgis_import_from(node, self.results)
