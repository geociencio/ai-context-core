"""Detects i18n usage and translatable strings."""

import ast
from typing import Dict, Any
from .base import BaseQGISChecker

from .i18n_components import is_translatable_string, handle_i18n_call


class I18nChecker(BaseQGISChecker):
    """Analyzes tr()/translate() usage and translatable string coverage.

    Delegates string classification and call handling to specialized components.
    """

    def __init__(self, results: Dict[str, Any]):
        super().__init__(results)
        self._in_ignored_call = False
        self._ignored_functions = {
            "debug",
            "info",
            "warning",
            "error",
            "critical",
            "log",
            "Exception",
            "ValueError",
            "TypeError",
            "RuntimeError",
        }

    def set_ignored(self, ignored: bool):
        """Sets whether the current context is an ignored call (e.g. logging)."""
        self._in_ignored_call = ignored

    def visit(self, node: ast.AST) -> None:
        """Visits nodes to detect i18n markers and translatable strings."""
        if isinstance(node, ast.Call):
            handle_i18n_call(node, self.results)
        elif isinstance(node, ast.Constant):
            self._check_constant(node)

    def _check_constant(self, node: ast.Constant):
        """Processes a string constant to determine translatability."""
        if not isinstance(node.value, str):
            return
        if self._in_ignored_call:
            return

        if is_translatable_string(node.value):
            self.results["i18n_usage"]["total_strings"] += 1

    def is_ignored_func(self, name: str) -> bool:
        """Checks if a function name should be ignored for translatable strings."""
        return name in self._ignored_functions
