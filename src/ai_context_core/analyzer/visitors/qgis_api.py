import ast
from typing import Dict, Any
from .qgis_base import BaseQGISChecker


class QGISApiChecker(BaseQGISChecker):
    """Checker for QGIS 3.x deprecated APIs and QGIS 4.x (Qt6) readiness."""

    DEPRECATED_APIS = {
        "QgsMapLayerRegistry": "Removed in QGIS 3. Use QgsProject.instance() instead.",
        "QGis": "Deprecated in favor of QgsUnitTypes and other modern namespaces.",
        "setDataProvider": "Deprecated on QgsRasterLayer. Use constructor or other methods.",
    }

    QT6_INCOMPATIBLE = {
        "SIGNAL": "Legacy macro removed in Qt6. Use native signals.",
        "SLOT": "Legacy macro removed in Qt6. Use decorators or native slots.",
    }

    def __init__(self, results: Dict[str, Any]):
        """Initialize the checker."""
        super().__init__(results)
        if "api_compatibility" not in self.results:
            self.results["api_compatibility"] = {
                "deprecated_calls": [],
                "qt6_incompatibilities": [],
                "best_practice_violations": [],
            }

    def visit(self, node: ast.AST) -> None:
        """Scan nodes for API usage."""
        if isinstance(node, ast.Call):
            self._check_call(node)
        elif isinstance(node, ast.Attribute):
            self._check_attribute(node)
        elif isinstance(node, ast.Name):
            self._check_name(node)

    def _check_call(self, node: ast.Call):
        """Check function calls for deprecated methods and legacy macros."""
        func_name = self._get_name(node.func)
        if func_name in self.DEPRECATED_APIS:
            self.results["api_compatibility"]["deprecated_calls"].append(
                {"name": func_name, "reason": self.DEPRECATED_APIS[func_name]}
            )

        if func_name in self.QT6_INCOMPATIBLE:
            self.results["api_compatibility"]["qt6_incompatibilities"].append(
                {"name": func_name, "reason": self.QT6_INCOMPATIBLE[func_name]}
            )

        # Check for iface.activeLayer() -> suggested iface.layerTreeView().currentLayer()
        if isinstance(node.func, ast.Attribute):
            if (
                node.func.attr == "activeLayer"
                and self._get_name(node.func.value) == "iface"
            ):
                self.results["api_compatibility"]["best_practice_violations"].append(
                    {
                        "name": "iface.activeLayer()",
                        "suggestion": "Use iface.layerTreeView().currentLayer() for better reliability.",
                    }
                )

    def _check_attribute(self, node: ast.Attribute):
        """Check attribute access for deprecated classes and legacy macros."""
        if node.attr in self.DEPRECATED_APIS:
            self.results["api_compatibility"]["deprecated_calls"].append(
                {"name": node.attr, "reason": self.DEPRECATED_APIS[node.attr]}
            )

        if node.attr in self.QT6_INCOMPATIBLE:
            self.results["api_compatibility"]["qt6_incompatibilities"].append(
                {"name": node.attr, "reason": self.QT6_INCOMPATIBLE[node.attr]}
            )

    def _check_name(self, node: ast.Name):
        """Check for deprecated global names and legacy macros."""
        if node.id in self.DEPRECATED_APIS:
            self.results["api_compatibility"]["deprecated_calls"].append(
                {"name": node.id, "reason": self.DEPRECATED_APIS[node.id]}
            )

        if node.id in self.QT6_INCOMPATIBLE:
            self.results["api_compatibility"]["qt6_incompatibilities"].append(
                {"name": node.id, "reason": self.QT6_INCOMPATIBLE[node.id]}
            )

        if node.id == "QSettings":
            self.results["api_compatibility"]["best_practice_violations"].append(
                {
                    "name": "QSettings",
                    "suggestion": "Use QgsSettings for automatic QGIS profile compatibility.",
                }
            )

    def _get_name(self, node: ast.AST) -> str:
        """Helper to get name from AST nodes."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""
