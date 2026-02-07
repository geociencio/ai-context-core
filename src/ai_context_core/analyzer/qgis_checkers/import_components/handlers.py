"""Logic for detecting GDAL and Qt import styles."""

import ast
from typing import Dict, Any


def handle_qgis_import(node: ast.Import, results: Dict[str, Any]) -> None:
    """Processes a standard import node for QGIS compliance."""
    for alias in node.names:
        _check_gdal_import(alias.name, results)
        _check_qt_transition(alias.name, results)


def handle_qgis_import_from(node: ast.ImportFrom, results: Dict[str, Any]) -> None:
    """Processes an import-from node for QGIS compliance."""
    if node.module == "osgeo" and any(a.name == "gdal" for a in node.names):
        results["gdal_import_style"] = "Correct"

    if node.module:
        _check_qt_transition(node.module, results)


def _check_gdal_import(name: str, results: Dict[str, Any]) -> None:
    """Checks if GDAL is imported the legacy way."""
    if name == "gdal":
        results["gdal_import_style"] = "Legacy"


def _check_qt_transition(module_name: str, results: Dict[str, Any]) -> None:
    """Checks for PyQt5/6 usage to aid transition."""
    if module_name.startswith("PyQt5"):
        results["qt_transition"]["pyqt5_imports"].append(module_name)
    elif module_name.startswith("PyQt6"):
        results["qt_transition"]["pyqt6_imports"].append(module_name)
