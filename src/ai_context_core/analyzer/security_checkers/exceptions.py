"""Detects insecure exception handling and assertions."""

import ast
from typing import List, Dict, Any
from .base import BaseSecurityChecker

class ExceptionsChecker(BaseSecurityChecker):
    """Detects use of assert in production and broad exception handlers."""

    def check(self, node: ast.AST, issues: List[Dict[str, Any]]) -> None:
        if isinstance(node, ast.Assert):
            issues.append({
                "pattern": "assert",
                "severity": "low",
                "line": node.lineno,
                "description": "Use of assert in production code",
            })
        elif isinstance(node, ast.ExceptHandler):
            self._check_except_handler(node, issues)

    def _check_except_handler(self, node: ast.ExceptHandler, issues: List[Dict[str, Any]]) -> None:
        if node.type is None:
            issues.append({
                "pattern": "except:",
                "severity": "medium",
                "line": node.lineno,
                "description": "Generic exception handler",
            })
        elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
            issues.append({
                "pattern": "except Exception:",
                "severity": "low",
                "line": node.lineno,
                "description": "Too broad exception handler",
            })
