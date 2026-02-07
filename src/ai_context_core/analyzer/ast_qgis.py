"""QGIS specific compliance and pattern detection."""

import ast
from typing import Dict, Any


class QGISComplianceVisitor(ast.NodeVisitor):
    """Visitor to check for QGIS coding standards and best practices."""

    def __init__(self):
        """Initialize the QGIS compliance visitor."""
        self.results = {
            "processing_framework": False,
            "i18n_usage": {"tr": 0, "translate": 0, "total_strings": 0},
            "gdal_import_style": "Modern",  # Modern, Legacy, or Missing
            "qt_transition": {"pyqt5_imports": [], "pyqt6_imports": []},
            "signals_slots": {"legacy": 0, "modern": 0},
        }
        self._in_ignored_call = False
        self._ignored_functions = {
            "debug",
            "info",
            "warning",
            "error",
            "critical",
            "log",  # Loggers
            "Exception",
            "ValueError",
            "TypeError",
            "RuntimeError",  # Exceptions
        }

    def visit_Import(self, node: ast.Import):
        """Visits an import node and checks for legacy GDAL or PyQt imports.

        Args:
            node: The Import node.
        """
        for alias in node.names:
            if alias.name == "gdal":
                self.results["gdal_import_style"] = "Legacy"
            if alias.name.startswith("PyQt5"):
                self.results["qt_transition"]["pyqt5_imports"].append(alias.name)
            if alias.name.startswith("PyQt6"):
                self.results["qt_transition"]["pyqt6_imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Visits an import-from node and checks for osgeo.gdal or PyQt.

        Args:
            node: The ImportFrom node.
        """
        if node.module == "osgeo" and any(a.name == "gdal" for a in node.names):
            self.results["gdal_import_style"] = "Correct"
        if node.module and node.module.startswith("PyQt5"):
            self.results["qt_transition"]["pyqt5_imports"].append(node.module)
        if node.module and node.module.startswith("PyQt6"):
            self.results["qt_transition"]["pyqt6_imports"].append(node.module)
        self.generic_visit(node)

    def visit_Module(self, node: ast.Module):
        """Visits the module node and ignores its docstring."""
        self._generic_visit_with_docstring_skip(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits a class definition and ignores its docstring."""
        # Check for Processing Framework (existing logic)
        processing_bases = {"QgsProcessingAlgorithm", "QgsProcessingProvider"}
        for base in node.bases:
            base_name = "Unknown"
            if isinstance(base, ast.Name):
                base_name = base.id
            elif isinstance(base, ast.Attribute):
                base_name = base.attr
            if base_name in processing_bases:
                self.results["processing_framework"] = True

        self._generic_visit_with_docstring_skip(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits a function definition and ignores its docstring."""
        self._generic_visit_with_docstring_skip(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visits an async function definition and ignores its docstring."""
        self._generic_visit_with_docstring_skip(node)

    def _generic_visit_with_docstring_skip(self, node: ast.AST):
        """Helper to visit children while skipping the docstring of the current node."""
        docstring = ast.get_docstring(node, clean=False)
        body = getattr(node, "body", [])
        start_idx = 0
        if docstring is not None and body and isinstance(body[0], ast.Expr):
            # Skip the first expression if it's the docstring
            start_idx = 1

        for child in body[start_idx:]:
            self.visit(child)

        # Visit decorators and other parts if applicable (for classes/functions)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for decorator in node.decorator_list:
                self.visit(decorator)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.args:
                    self.visit(arg)
                if node.returns:
                    self.visit(node.returns)
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    self.visit(base)

    def visit_Call(self, node: ast.Call):
        """Visits a call node to detect i18n usage and legacy signals.

        Args:
            node: The Call node.
        """
        # Detect if we should ignore strings inside this call
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        old_ignored = self._in_ignored_call
        if func_name in self._ignored_functions:
            self._in_ignored_call = True

        # Check for i18n: self.tr() or QCoreApplication.translate()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "tr":
                self.results["i18n_usage"]["tr"] += 1
            elif node.func.attr == "translate":
                # Check for QCoreApplication.translate or simply .translate
                self.results["i18n_usage"]["translate"] += 1

        # Check for legacy signals/slots (SIGNAL/SLOT macros)
        if isinstance(node.func, ast.Name) and node.func.id in ("SIGNAL", "SLOT"):
            self.results["signals_slots"]["legacy"] += 1

        self.generic_visit(node)
        self._in_ignored_call = old_ignored

    def visit_Constant(self, node: ast.Constant):
        """Visits a constant node to count potential i18n strings.

        Args:
            node: The Constant node.
        """
        if not isinstance(node.value, str) or len(node.value.strip()) <= 1:
            return

        if self._in_ignored_call:
            return

        val = node.value.strip()

        # Filter out common technical strings
        is_path = val.startswith(("/", "./", "../")) or "\\" in val
        is_url = val.startswith(("http://", "https://", "ftp://"))
        is_placeholder = val.replace("{}", "").replace("%s", "").strip() == ""

        if not (is_path or is_url or is_placeholder):
            # Heuristic: strings with spaces or punctuation are usually translatable.
            if " " in val or any(c in val for c in ".,!?;"):
                self.results["i18n_usage"]["total_strings"] += 1

        self.generic_visit(node)


def is_qgis_entry_point_node(node: ast.AST) -> bool:
    """Checks if an AST node is a QGIS classFactory entry point."""
    return (
        isinstance(node, ast.FunctionDef)
        and node.name == "classFactory"
        and any(arg.arg == "iface" for arg in node.args.args)
    )


def check_qgis_compliance(tree: ast.AST) -> Dict[str, Any]:
    """Checks for compliance with QGIS-specific coding standards.

    Analyzes i18n usage, Qt transition preparation, and Processing Framework patterns.

    Args:
        tree: The AST to analyze.

    Returns:
        Dictionary of QGIS-specific metrics and findings.
    """
    visitor = QGISComplianceVisitor()
    visitor.visit(tree)
    return visitor.results
