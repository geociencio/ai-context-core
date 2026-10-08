"""Detects SQL and Command injection vulnerabilities."""

import ast
from typing import List, Dict, Any
from .security_base import BaseSecurityChecker
from .injection_os import OSCommandRule
from .injection_sql import SQLInjectionRule


class InjectionChecker(BaseSecurityChecker):
    """Detects potential SQL and command injection patterns.

    Delegates checks to specialized rule classes for OS commands and SQL.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the checker with rules."""
        super().__init__(config)
        self.os_rule = OSCommandRule()
        self.sql_rule = SQLInjectionRule()

    def check(self, node: ast.AST, issues: List[Dict[str, Any]]) -> None:
        """Orchestrates injection checks on AST nodes."""
        if isinstance(node, ast.Call):
            self.os_rule.check(node, issues)
            self.sql_rule.check(node, issues)
        elif isinstance(node, ast.JoinedStr):
            self._check_joined_str(node, issues)

    def _check_joined_str(self, node: ast.JoinedStr, issues: List[Dict[str, Any]]) -> None:
        """Heuristic for f-string SQL outside of execute()."""
        if any(
            "SELECT" in str(v.value).upper() and "FROM" in str(v.value).upper()
            for v in node.values
            if isinstance(v, ast.Constant)
        ):
            if not any(i["line"] == node.lineno for i in issues):
                issues.append(
                    {
                        "pattern": "f-string SQL",
                        "severity": "high",
                        "line": node.lineno,
                        "description": "Possible SQL injection in f-string",
                    }
                )
