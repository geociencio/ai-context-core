"""OS command injection detection rule."""

import ast
from typing import List, Dict, Any


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
            issues.append(
                {
                    "pattern": "os.system",
                    "severity": "high",
                    "line": node.lineno,
                    "description": "os.system() usage - potential command injection",
                }
            )
        elif module_name == "subprocess" and attr_name in ("call", "Popen", "run"):
            self._check_subprocess(node, issues)

    def _check_subprocess(self, node: ast.Call, issues: List[Dict[str, Any]]) -> None:
        """Checks subprocess calls for unsafe shell=True."""
        shell_true = any(
            kw.arg == "shell"
            and isinstance(kw.value, ast.Constant)
            and kw.value.value is True
            for kw in node.keywords
        )
        if shell_true:
            attr = node.func.attr if isinstance(node.func, ast.Attribute) else "unknown"
            issues.append(
                {
                    "pattern": f"subprocess.{attr}",
                    "severity": "high",
                    "line": node.lineno,
                    "description": f"subprocess.{attr}() with shell=True - potential command injection",
                }
            )
