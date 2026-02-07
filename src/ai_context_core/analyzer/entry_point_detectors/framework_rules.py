"""Specialized rules for detecting framework entry points."""

import ast
from typing import Optional
from .base import BaseEntryPointRule

class DecoratorRule(BaseEntryPointRule):
    """Detects entry points based on function decorators (click, flask, fastapi)."""

    def check(self, node: ast.AST) -> Optional[str]:
        if not isinstance(node, (ast.Call, ast.Attribute, ast.Name)):
            return None
            
        check_node = node.func if isinstance(node, ast.Call) else node
        if not isinstance(check_node, ast.Attribute):
            return None
        
        attr = check_node.attr
        val = check_node.value
        if isinstance(val, ast.Name):
            if val.id == "click" and attr in ("command", "group"):
                return "click_cli"
            if attr == "route":
                return "flask_app"
            if attr in ("get", "post", "put", "delete", "patch"):
                return "fastapi_app"
        return None

class AssignmentRule(BaseEntryPointRule):
    """Detects entry points based on variable assignments (django, flask, fastapi)."""

    def __init__(self, target_id: str, value: ast.AST):
        self.target_id = target_id
        self.value = value

    def check(self, node: ast.AST) -> Optional[str]:
        if self.target_id == "application":
            return "django_app"
        if self.target_id == "urlpatterns" and isinstance(self.value, (ast.List, ast.Tuple)):
            return "django_urls"
        if self.target_id == "INSTALLED_APPS" and isinstance(self.value, (ast.List, ast.Tuple)):
            return "django_settings"
        
        if self.target_id in ("app", "application") and isinstance(self.value, ast.Call):
            func = self.value.func
            if isinstance(func, ast.Name):
                if func.id == "Flask":
                    return "flask_app"
                if func.id == "FastAPI":
                    return "fastapi_app"
        return None
