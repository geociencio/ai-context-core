"""Checker for import style compliance (GDAL, PyQt, etc.)."""

import ast
from typing import Dict, Any
from .qgis_base import BaseQGISChecker
from .imports_visitor import (  # noqa: F401
    ImportVisitor,
    extract_imports,
    detect_unused_imports,
)


class ImportStyleChecker(BaseQGISChecker):
    """Checker for import style compliance (GDAL, PyQt, etc.)."""

    def __init__(self, results: Dict[str, Any]):
        """Initialize the checker with results dict."""
        super().__init__(results)

    def visit(self, node: ast.AST):
        """Visit a node to check import style."""
        if isinstance(node, ast.Import):
            self.visit_Import(node)
        elif isinstance(node, ast.ImportFrom):
            self.visit_ImportFrom(node)

    def visit_Import(self, node: ast.Import):
        """Check import statements."""
        for alias in node.names:
            # Check for GDAL imports
            if alias.name.startswith("osgeo"):
                self.results["gdal_import_style"] = "Correct"
            elif alias.name == "gdal":
                self.results["gdal_import_style"] = "Legacy"

            # Check for PyQt imports
            if alias.name.startswith("PyQt5"):
                if alias.name not in self.results["qt_transition"]["pyqt5_imports"]:
                    self.results["qt_transition"]["pyqt5_imports"].append(alias.name)
            elif alias.name.startswith("PyQt6"):
                if alias.name not in self.results["qt_transition"]["pyqt6_imports"]:
                    self.results["qt_transition"]["pyqt6_imports"].append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Check from-import statements."""
        if node.module:
            # Check for GDAL imports
            if node.module.startswith("osgeo"):
                self.results["gdal_import_style"] = "Correct"
            elif node.module == "gdal":
                self.results["gdal_import_style"] = "Legacy"

            # Check for PyQt imports - track the module being imported from
            if node.module.startswith("PyQt5"):
                # Add the module itself, not individual imports
                if node.module not in self.results["qt_transition"]["pyqt5_imports"]:
                    self.results["qt_transition"]["pyqt5_imports"].append(node.module)
            elif node.module.startswith("PyQt6"):
                if node.module not in self.results["qt_transition"]["pyqt6_imports"]:
                    self.results["qt_transition"]["pyqt6_imports"].append(node.module)
