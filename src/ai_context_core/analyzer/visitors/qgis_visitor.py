"""Visitor implementation for QGIS compliance analysis."""

import ast


from .visitors_base import BaseVisitor


class GenericQGISComplianceVisitor(BaseVisitor):
    """Visitor to check for QGIS coding standards and best practices."""

    def __init__(self):
        """Initialize the visitor with default results and checkers."""
        super().__init__()
        self.results = {
            "processing_framework": False,
            "i18n_usage": {"tr": 0, "translate": 0, "total_strings": 0},
            "gdal_import_style": "Modern",
            "qt_transition": {"pyqt5_imports": [], "pyqt6_imports": []},
            "signals_slots": {"legacy": 0, "modern": 0},
        }
        from .imports import ImportStyleChecker
        from .i18n import I18nChecker
        from .frameworks import FrameworkChecker
        from .qgis_api import QGISApiChecker

        self.checkers = [
            ImportStyleChecker(self.results),
            I18nChecker(self.results),
            FrameworkChecker(self.results),
            QGISApiChecker(self.results),
        ]
        self._i18n_checker = next(
            c for c in self.checkers if isinstance(c, I18nChecker)
        )

    def visit_Import(self, node: ast.Import):
        """Checks for legacy imports."""
        for checker in self.checkers:
            if hasattr(checker, "visit_Import"):
                checker.visit_Import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Checks for osgeo or PyQt imports."""
        for checker in self.checkers:
            if hasattr(checker, "visit_ImportFrom"):
                checker.visit_ImportFrom(node)
        self.generic_visit(node)

    def visit_Module(self, node: ast.Module):
        """Visits module while skipping docstring."""
        self._get_base_checker().generic_visit_with_docstring_skip(self, node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits class while skipping docstring."""
        for checker in self.checkers:
            checker.visit(node)
        self._get_base_checker().generic_visit_with_docstring_skip(self, node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits function while skipping docstring."""
        self._get_base_checker().generic_visit_with_docstring_skip(self, node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visits async function while skipping docstring."""
        self._get_base_checker().generic_visit_with_docstring_skip(self, node)

    def _get_base_checker(self):
        """Returns the first checker which inherits from BaseQGISChecker."""
        return self.checkers[0]

    def visit_Call(self, node: ast.Call):
        """Visits a call node to detect i18n usage and legacy signals."""
        func_name = self._get_func_name(node.func)
        is_ignored_func = self._i18n_checker.is_ignored_func(func_name)

        if is_ignored_func:
            self._i18n_checker.set_ignored(True)

        for checker in self.checkers:
            checker.visit(node)

        self.generic_visit(node)

        if is_ignored_func:
            self._i18n_checker.set_ignored(False)

    def _get_func_name(self, func: ast.expr) -> str:
        """Helper to get the name of a called function."""
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
        return ""

    def visit_Dict(self, node: ast.Dict):
        """Visits dictionary and ignores its keys for i18n string counting."""
        for key, value in zip(node.keys, node.values):
            if key:
                self._i18n_checker.set_in_dict(True)
                self.visit(key)
                self._i18n_checker.set_in_dict(False)
            if value:
                self.visit(value)

    def visit_Constant(self, node: ast.Constant):
        """Visits a constant node to count potential i18n strings."""
        self._i18n_checker.visit(node)
        self.generic_visit(node)
