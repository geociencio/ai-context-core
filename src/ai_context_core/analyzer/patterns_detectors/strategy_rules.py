"""Specialized rules for detecting Strategy pattern indicators."""

import ast


class StrategyRules:
    """Encapsulates patterns for Strategy detection."""

    INJECTION_KEYWORDS = ("strategy", "algorithm", "engine", "handler", "mode")
    CALL_KEYWORDS = ("strategy", "algorithm", "engine", "handler")

    @classmethod
    def check_injection(cls, node: ast.FunctionDef) -> str:
        """Checks if a method has strategy injection in its arguments.

        Args:
            node: The FunctionDef node to check.

        Returns:
            The name of the argument if found, else empty string.
        """
        for arg in node.args.args:
            if any(kw in arg.arg.lower() for kw in cls.INJECTION_KEYWORDS):
                return arg.arg
        return ""

    @classmethod
    def detect_strategy_call(cls, node: ast.FunctionDef) -> str:
        """Detects calls to strategy objects within a method.

        Args:
            node: The method body to analyze.

        Returns:
            The unparsed function call if detected, else empty string.
        """
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                unparsed = ast.unparse(sub.func).lower()
                if any(kw in unparsed for kw in cls.CALL_KEYWORDS):
                    return ast.unparse(sub.func)
        return ""
