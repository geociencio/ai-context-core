"""Static analysis tools for identifying technical debt and security risks.

Includes rule-based detection for complexity hotspots, large modules,
security patterns, and optimization opportunities.

This module now uses a plugin-based system with Checkers.
"""

import ast
import warnings
from typing import List, Dict, Any

from .ast_security import ASTSecurityDetector, IssueDetector  # noqa: F401


from .checker_registry import CheckerRegistry
from .secrets_scanner import find_secrets
from .optimizations import find_optimizations  # noqa: F401
from .debt import find_technical_debt  # noqa: F401
from ..registry import register_detector


class GenericIssueDetector:
    """Base class for issue detection rules (Legacy)."""

    @property
    def detector_class(self):

        return ASTSecurityDetector

    def detect(self, **kwargs) -> List[Dict[str, Any]]:
        """Static analysis tool for identifying issues.

        Args:
            **kwargs: Analysis-specific arguments.

        Returns:
            List of detected issues.
        """
        raise NotImplementedError


def run_analysis(
    module_info: Dict[str, Any], config: Dict[str, Any] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Run all registered checkers on a module.

    Args:
        module_info: Analyzed module data.
        config: Optional configuration.

    Returns:
        Dictionary mapping category to list of found issues.
    """
    return CheckerRegistry.run_all(module_info, config)


def find_security_issues(
    modules_data: List[Dict[str, Any]], project_path: str
) -> List[Dict[str, Any]]:
    """Find security issues in project modules (DEPRECATED).

    Args:
        modules_data: List of module data.
        project_path: Path to the project root.

    Returns:
        List of security issues.
    """
    warnings.warn(
        "find_security_issues is deprecated. Use find_secrets or AST detection.",
        DeprecationWarning,
        stacklevel=2,
    )
    return find_secrets(modules_data, project_path)


@register_detector("ast_security")
def detect(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects security issues in the AST.

    Args:
        tree: The AST to analyze.

    Returns:
        List of detected security issues.
    """
    from .ast_security import detect_ast_security_issues as _detect_ast_security

    return _detect_ast_security(tree)


# Alias for backward compatibility (used in tests)
def detect_ast_security_issues(tree: ast.AST) -> List[Dict[str, Any]]:
    """Legacy wrapper for AST security detection."""
    return detect(tree)
