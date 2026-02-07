"""Security vulnerability detection using AST analysis."""

import ast
from typing import List, Dict, Any


class IssueDetector:
    """Base class for issue detection rules."""

    def detect(self, **kwargs) -> List[Dict[str, Any]]:
        """Analyzes a node or tree and returns detected issues.

        Args:
            **kwargs: Implementation-specific arguments (usually 'tree' or 'node').

        Returns:
            A list of detected security issues.
        """
        raise NotImplementedError


class ASTSecurityDetector(IssueDetector):
    """Detects security issues using AST analysis.

    Orchestrates multiple specialized checkers to identify common vulnerabilities
    like SQL injection, command injection, and insecure function usage.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize detector with configuration.

        Args:
            config: Configuration dictionary containing security patterns.
        """
        self.config = config or {}
        from .security_checkers import InjectionChecker, InsecureCallsChecker, ExceptionsChecker
        self.checkers = [
            InjectionChecker(self.config),
            InsecureCallsChecker(self.config),
            ExceptionsChecker(self.config),
        ]

    def detect(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyzes an AST for common security vulnerabilities.

        Args:
            tree: The AST to analyze.

        Returns:
            List of detected security issues with line numbers and severity.
        """
        issues = []
        for node in ast.walk(tree):
            for checker in self.checkers:
                checker.check(node, issues)
        return issues


def detect_ast_security_issues(tree: ast.AST) -> List[Dict[str, Any]]:
    """Legacy wrapper for AST security detection.

    Args:
        tree: The AST to analyze.

    Returns:
        List of detected security issues.
    """
    return ASTSecurityDetector({}).detect(tree)
