"""Detects QGIS framework usage like Processing and Signals/Slots."""

import ast
from .base import BaseQGISChecker


class FrameworkChecker(BaseQGISChecker):
    """Checks for Processing framework and Signals/Slots usage patterns."""

    def visit(self, node: ast.AST) -> None:
        if isinstance(node, ast.ClassDef):
            self._check_processing_framework(node)
        elif isinstance(node, ast.Call):
            self._check_signals_slots(node)

    def _check_processing_framework(self, node: ast.ClassDef):
        processing_bases = {"QgsProcessingAlgorithm", "QgsProcessingProvider"}
        for base in node.bases:
            name = self._get_name(base)
            if name in processing_bases:
                self.results["processing_framework"] = True
                break

    def _check_signals_slots(self, node: ast.Call):
        name = self._get_name(node.func)
        if name in ("SIGNAL", "SLOT"):
            self.results["signals_slots"]["legacy"] += 1

    def _get_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""
