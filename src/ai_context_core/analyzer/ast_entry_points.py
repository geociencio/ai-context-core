"""Entry point detection for various frameworks (QGIS, Click, Flask, FastAPI)."""

import ast
from typing import Dict, Any
from .ast_qgis import is_qgis_entry_point_node


class EntryPointVisitor(ast.NodeVisitor):
    """Visitor to detect if a module is an entry point."""

    def __init__(self):
        self.result = {"is_entry_point": False, "type": None}

    def visit_If(self, node: ast.If):
        if self.result["is_entry_point"]:
            return

        # Check for if __name__ == "__main__":
        try:
            if (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
            ):
                for comparator in node.test.comparators:
                    if (
                        isinstance(comparator, ast.Constant)
                        and comparator.value == "__main__"
                    ):
                        self.result = {"is_entry_point": True, "type": "main_guard"}
                        return
        except Exception:
            pass
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.result["is_entry_point"]:
            return

        # QGIS classFactory
        if is_qgis_entry_point_node(node):
            self.result = {"is_entry_point": True, "type": "qgis_plugin"}
            return

        # Check decorators
        for decorator in node.decorator_list:
            self._check_decorator(decorator)
            if self.result["is_entry_point"]:
                return

        self.generic_visit(node)

    def _check_decorator(self, decorator: ast.AST):
        check_node = decorator
        if isinstance(decorator, ast.Call):
            check_node = decorator.func

        if isinstance(check_node, ast.Attribute):
            attr = check_node.attr
            # Click
            if (
                isinstance(check_node.value, ast.Name)
                and check_node.value.id == "click"
                and attr in ("command", "group")
            ):
                self.result = {"is_entry_point": True, "type": "click_cli"}
            # Flask
            elif attr == "route":
                self.result = {"is_entry_point": True, "type": "flask_app"}
            # FastAPI
            elif attr in ("get", "post", "put", "delete", "patch"):
                self.result = {"is_entry_point": True, "type": "fastapi_app"}

    def visit_Assign(self, node: ast.Assign):
        if self.result["is_entry_point"]:
            return

        for target in node.targets:
            if isinstance(target, ast.Name):
                self._check_assignment(target.id, node.value)
                if self.result["is_entry_point"]:
                    return
        self.generic_visit(node)

    def _check_assignment(self, target_id: str, value_node: ast.AST):
        # Django
        if target_id == "application":
            self.result = {"is_entry_point": True, "type": "django_app"}
        elif target_id == "urlpatterns" and isinstance(
            value_node, (ast.List, ast.Tuple)
        ):
            self.result = {"is_entry_point": True, "type": "django_urls"}
        elif target_id == "INSTALLED_APPS" and isinstance(
            value_node, (ast.List, ast.Tuple)
        ):
            self.result = {"is_entry_point": True, "type": "django_settings"}

        # Flask/FastAPI instantiation i.e. app = Flask(__name__)
        elif target_id in ("app", "application") and isinstance(value_node, ast.Call):
            func = value_node.func
            if isinstance(func, ast.Name):
                if func.id == "Flask":
                    self.result = {"is_entry_point": True, "type": "flask_app"}
                elif func.id == "FastAPI":
                    self.result = {"is_entry_point": True, "type": "fastapi_app"}


def is_entry_point(tree: ast.AST) -> Dict[str, Any]:
    """Determines if the module is an entry point."""
    visitor = EntryPointVisitor()
    visitor.visit(tree)
    return visitor.result


def has_main_guard(tree: ast.AST) -> bool:
    """Checks if the module contains the standard 'if __name__ == "__main__":' guard."""
    result = is_entry_point(tree)
    return result["is_entry_point"] and result["type"] == "main_guard"
