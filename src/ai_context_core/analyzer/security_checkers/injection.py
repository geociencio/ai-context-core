"""Detects SQL and Command injection vulnerabilities."""

import ast
from typing import List, Dict, Any
from .base import BaseSecurityChecker

class OSCommandRule:
    """Detects OS command injection vulnerabilities."""

    def check(self, node: ast.Call, issues: List[Dict[str, Any]]) -> None:
        """Analyzes a call node for OS command injections."""
        func = node.func
        if not isinstance(func, ast.Attribute) or not isinstance(func.value, ast.Name):
            return

        module_name = func.value.id
        attr_name = func.attr

        if module_name == "os" and attr_name == "system":
            issues.append({
                "pattern": "os.system",
                "severity": "high",
                "line": node.lineno,
                "description": "os.system() usage - potential command injection",
            })
        elif module_name == "subprocess" and attr_name in ("call", "Popen", "run"):
            self._check_subprocess(node, issues)

    def _check_subprocess(self, node: ast.Call, issues: List[Dict[str, Any]]) -> None:
        """Checks subprocess calls for unsafe shell=True."""
        shell_true = any(
            kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True
            for kw in node.keywords
        )
        if shell_true:
            attr = node.func.attr if isinstance(node.func, ast.Attribute) else "unknown"
            issues.append({
                "pattern": f"subprocess.{attr}",
                "severity": "high",
                "line": node.lineno,
                "description": f"subprocess.{attr}() with shell=True - potential command injection",
            })


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
        elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == "format":
            self._check_format(node, arg, issues)
        elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
            self._check_percent(node, arg, issues)

    def _check_fstring(self, node: ast.Call, arg: ast.JoinedStr, issues: List[Dict[str, Any]]) -> None:
        if any("SELECT" in str(v.value).upper() for v in arg.values if isinstance(v, ast.Constant)):
            issues.append({
                "pattern": "SQL Injection (f-string)",
                "severity": "critical",
                "line": node.lineno,
                "description": "Unsafe SQL construction using f-string in execute()",
            })

    def _check_format(self, node: ast.Call, arg: ast.Call, issues: List[Dict[str, Any]]) -> None:
        if isinstance(arg.func.value, ast.Constant) and "SELECT" in str(arg.func.value.value).upper():
            issues.append({
                "pattern": "SQL Injection (.format)",
                "severity": "high",
                "line": node.lineno,
                "description": "Unsafe SQL construction using .format() in execute()",
            })

    def _check_percent(self, node: ast.Call, arg: ast.BinOp, issues: List[Dict[str, Any]]) -> None:
        if isinstance(arg.left, ast.Constant) and "SELECT" in str(arg.left.value).upper():
            issues.append({
                "pattern": "SQL Injection (%)",
                "severity": "high",
                "line": node.lineno,
                "description": "Unsafe SQL construction using % in execute()",
            })


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
                issues.append({
                    "pattern": "f-string SQL",
                    "severity": "high",
                    "line": node.lineno,
                    "description": "Possible SQL injection in f-string",
                })
