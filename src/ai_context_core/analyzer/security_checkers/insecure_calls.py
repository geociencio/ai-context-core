"""Detects dangerous function and module calls."""

import ast
from typing import List, Dict, Any
from .base import BaseSecurityChecker

class InsecureCallsChecker(BaseSecurityChecker):
    """Detects usage of dangerous functions like eval, exec, and insecure modules."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        patterns = self.config.get("security_patterns", {})
        self.dangerous_functions = set(
            patterns.get("dangerous_functions", ["exec", "eval", "__import__", "input"])
        )
        self.dangerous_modules = set(
            patterns.get("dangerous_modules", ["pickle", "marshal", "telnetlib"])
        )

    def check(self, node: ast.AST, issues: List[Dict[str, Any]]) -> None:
        if not isinstance(node, ast.Call):
            return

        if isinstance(node.func, ast.Name):
            if node.func.id in self.dangerous_functions:
                issues.append({
                    "pattern": node.func.id,
                    "severity": "high",
                    "line": node.lineno,
                    "description": f"{node.func.id}() usage - potential security risk",
                })
        elif isinstance(node.func, ast.Attribute):
            self._check_attribute_call(node, issues)

    def _check_attribute_call(self, node: ast.Call, issues: List[Dict[str, Any]]) -> None:
        func = node.func
        if not isinstance(func, ast.Attribute) or not isinstance(func.value, ast.Name):
            return

        module_name = func.value.id
        attr_name = func.attr

        if module_name in self.dangerous_modules:
            issues.append({
                "pattern": f"{module_name}.{attr_name}",
                "severity": "high",
                "line": node.lineno,
                "description": f"{module_name} usage - possible insecure deserialization",
            })
