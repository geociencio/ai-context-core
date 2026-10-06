"""Detects i18n usage and translatable strings."""

import ast
from typing import Dict, Any
from .qgis_base import BaseQGISChecker

from .i18n_components import is_translatable_string, handle_i18n_call

# Functions whose string arguments are technical and must never be counted.
DEFAULT_IGNORED_FUNCTIONS = frozenset(
    {
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
        "setObjectName",
        "addItem",
        "setValue",
        "value",
        "key",
        "setProperty",
        "connect",
        "disconnect",
        "signal",
        "slot",
    }
)

# User-facing UI setter APIs whose string arguments are always translatable,
# even when the generic heuristics would reject them (short or CamelCase labels).
DEFAULT_UI_FUNCTIONS = frozenset(
    {
        "setText",
        "setTitle",
        "setWindowTitle",
        "setToolTip",
        "setWhatsThis",
        "setPlaceholderText",
        "setStatusTip",
        "setItemText",
        "setHeaderData",
        "setAccessibleName",
        "setTabText",
    }
)


class I18nChecker(BaseQGISChecker):
    """Analyzes tr()/translate() usage and translatable string coverage.

    Delegates string classification and call handling to specialized components.
    The ignore and UI allowlists are overridable for per-project tuning.
    """

    def __init__(
        self,
        results: Dict[str, Any],
        no_i18n_lines=None,
        ignored_functions=None,
        ui_functions=None,
    ):
        """Initialize the checker.

        Args:
            results: Shared results dictionary for i18n counters.
            no_i18n_lines: Line numbers opted out via ``# no-i18n``.
            ignored_functions: Optional override of the technical denylist.
            ui_functions: Optional override of the user-facing UI allowlist.
        """
        super().__init__(results)
        self._no_i18n_lines = frozenset(no_i18n_lines or ())
        self._in_ignored_call = False
        self._in_dict_key = False
        self._in_ui_call = False
        self._ignored_functions = (
            frozenset(ignored_functions)
            if ignored_functions is not None
            else DEFAULT_IGNORED_FUNCTIONS
        )
        self._ui_functions = (
            frozenset(ui_functions) if ui_functions is not None else DEFAULT_UI_FUNCTIONS
        )

    def set_ignored(self, ignored: bool):
        """Sets whether the current context is an ignored call (e.g. logging)."""
        self._in_ignored_call = ignored

    def set_in_dict(self, in_dict: bool):
        """Sets whether the current context is a dictionary key."""
        self._in_dict_key = in_dict

    def set_ui_call(self, in_ui: bool):
        """Sets whether the current context is a user-facing UI setter call."""
        self._in_ui_call = in_ui

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
        if self._in_ignored_call or self._in_dict_key:
            return
        if node.lineno in self._no_i18n_lines:
            return

        # Strings passed to user-facing UI setters are always translatable.
        if self._in_ui_call:
            if node.value.strip():
                self.results["i18n_usage"]["total_strings"] += 1
            return

        if is_translatable_string(node.value):
            self.results["i18n_usage"]["total_strings"] += 1

    def is_ignored_func(self, name: str) -> bool:
        """Checks if a function name should be ignored for translatable strings."""
        return name in self._ignored_functions

    def is_ui_func(self, name: str) -> bool:
        """Checks if a function name is a user-facing UI setter."""
        return name in self._ui_functions
