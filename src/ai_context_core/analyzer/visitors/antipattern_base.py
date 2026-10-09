"""Base classes for anti-pattern detection."""

import ast
from typing import List, Dict, Any

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def severity_rank(severity: str) -> int:
    """Map a severity string to an ordering rank (lower is more severe)."""
    return SEVERITY_ORDER.get(severity, len(SEVERITY_ORDER))


def min_severity_from_config(config: Dict[str, Any]) -> str:
    """Extract the configured minimum anti-pattern severity (default ``low``)."""
    patterns = config.get("patterns") or {}
    return patterns.get("antipatterns", {}).get("min_severity", "low")


def filter_issues(issues: List[Dict[str, Any]], min_severity: str = "low") -> List[Dict[str, Any]]:
    """Filter issues to those at or above the given severity."""
    min_rank = severity_rank(min_severity)
    return [i for i in issues if severity_rank(i.get("severity", "low")) <= min_rank]


class AntiPatternDetector:
    """Base class for anti-pattern detectors."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the antipattern detector.

        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
        self.issues = []

    def detect(self, node: ast.AST) -> List[Dict[str, Any]]:
        """Analyzes a node and returns detected issue instances.

        Args:
            node: The AST node to analyze.

        Returns:
            A list of detected issues.
        """
        raise NotImplementedError

    def _add_issue(self, type_id: str, severity: str, msg: str, line: int, value: Any):
        """Adds a detected issue to the list.

        Args:
            type_id: Unique identifier for the issue type.
            severity: Issue severity (low, medium, high).
            msg: Descriptive message for the issue.
            line: Line number where the issue was detected.
            value: The value or metric related to the issue.
        """
        self.issues.append(
            {
                "type": type_id,
                "severity": severity,
                "message": msg,
                "line": line,
                "value": value,
            }
        )
