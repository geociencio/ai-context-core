"""Entry point detection for various frameworks (QGIS, Click, Flask, FastAPI)."""

import ast
from typing import Dict, Any
from .ast_qgis import is_qgis_entry_point_node


class EntryPointVisitor(ast.NodeVisitor):
    """Visitor to detect if a module is an entry point.

    Analyzes various patterns like __main__ guards, QGIS plugin entry points,
    and framework-specific decorators or assignments.
    """

    def __init__(self):
        """Initialize the entry point visitor."""
        self.result = {"is_entry_point": False, "type": None}
        from .entry_point_detectors import DecoratorRule

        self._deco_rule = DecoratorRule()

    def visit_If(self, node: ast.If):
        """Checks for __main__ guards."""
        if not self.result["is_entry_point"] and self._is_main_guard(node):
            self.result = {"is_entry_point": True, "type": "main_guard"}
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Checks for QGIS entry points or framework decorators."""
        if self.result["is_entry_point"]:
            return
        if is_qgis_entry_point_node(node):
            self.result = {"is_entry_point": True, "type": "qgis_plugin"}
            return
        for deco in node.decorator_list:
            res_type = self._deco_rule.check(deco)
            if res_type:
                self.result = {"is_entry_point": True, "type": res_type}
                return
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """Checks for application assignments (Django, Flask, FastAPI)."""
        if self.result["is_entry_point"]:
            return
        from .entry_point_detectors import AssignmentRule

        for target in node.targets:
            if isinstance(target, ast.Name):
                res_type = AssignmentRule(target.id, node.value).check(node)
                if res_type:
                    self.result = {"is_entry_point": True, "type": res_type}
                    return
        self.generic_visit(node)

    def _is_main_guard(self, node: ast.If) -> bool:
        """Heuristic for 'if __name__ == "__main__":'."""
        try:
            return (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                and any(
                    isinstance(c, ast.Constant) and c.value == "__main__"
                    for c in node.test.comparators
                )
            )
        except Exception:
            return False


def is_entry_point(tree: ast.AST) -> Dict[str, Any]:
    """Analyzes a module to determine if it acts as an entry point.

    Checks for __main__ guards and common CLI or QGIS plugin entry points.

    Args:
        tree: The AST to analyze.

    Returns:
        Dictionary with is_entry_point (bool) and entry_point_type (str).
    """
    visitor = EntryPointVisitor()
    visitor.visit(tree)
    return visitor.result


def has_main_guard(tree: ast.AST) -> bool:
    """Checks if the module contains the standard 'if __name__ == "__main__":' guard.

    Args:
        tree: The AST to analyze.

    Returns:
        True if a main guard is found.
    """
    result = is_entry_point(tree)
    return result["is_entry_point"] and result["type"] == "main_guard"
