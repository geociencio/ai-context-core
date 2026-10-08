"""SQL injection detection rule."""

import ast
from typing import List, Dict, Any


class SQLInjectionRule:
    """Detects SQL injection vulnerabilities in execute() calls."""

    def check(self, node: ast.Call, issues: List[Dict[str, Any]]) -> None:
        """Analyzes a call node for SQL injections."""
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr != "execute":
            return

        if not node.args:
            return
        arg = node.args[0]
        if isinstance(arg, ast.JoinedStr):
            self._check_fstring(node, arg, issues)
        elif (
            isinstance(arg, ast.Call)
            and isinstance(arg.func, ast.Attribute)
            and arg.func.attr == "format"
        ):
            self._check_format(node, arg, issues)
        elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
            self._check_percent(node, arg, issues)

    def _check_fstring(
        self, node: ast.Call, arg: ast.JoinedStr, issues: List[Dict[str, Any]]
    ) -> None:
        if any("SELECT" in str(v.value).upper() for v in arg.values if isinstance(v, ast.Constant)):
            issues.append(
                {
                    "pattern": "SQL Injection (f-string)",
                    "severity": "critical",
                    "line": node.lineno,
                    "description": "Unsafe SQL construction using f-string in execute()",
                }
            )

    def _check_format(self, node: ast.Call, arg: ast.Call, issues: List[Dict[str, Any]]) -> None:
        if (
            isinstance(arg.func.value, ast.Constant)
            and "SELECT" in str(arg.func.value.value).upper()
        ):
            issues.append(
                {
                    "pattern": "SQL Injection (.format)",
                    "severity": "high",
                    "line": node.lineno,
                    "description": "Unsafe SQL construction using .format() in execute()",
                }
            )

    def _check_percent(self, node: ast.Call, arg: ast.BinOp, issues: List[Dict[str, Any]]) -> None:
        if isinstance(arg.left, ast.Constant) and "SELECT" in str(arg.left.value).upper():
            issues.append(
                {
                    "pattern": "SQL Injection (%)",
                    "severity": "high",
                    "line": node.lineno,
                    "description": "Unsafe SQL construction using % in execute()",
                }
            )
