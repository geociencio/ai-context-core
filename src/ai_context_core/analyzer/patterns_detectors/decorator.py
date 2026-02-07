"""Decorator pattern detector implementation."""

import ast
from typing import Dict, List, Any
from .base import PatternDetector


from .decorator_rules import DecoratorRules


class DecoratorDetector(PatternDetector):
    """Detects Decorator pattern implementations.

    Delegates rule checking to DecoratorRules to keep complexity low.
    """

    def detect(self, node: ast.AST) -> List[Dict[str, Any]]:
        """Detects Decorator pattern implementations in a node.

        Args:
            node: The AST node to analyze.

        Returns:
            List of detected decorator instances.
        """
        res = []
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._analyze_function(node, res)
        elif isinstance(node, ast.ClassDef):
            self._analyze_class(node, res)
        return res

    def _analyze_function(self, node: ast.AST, res: List[Dict[str, Any]]) -> None:
        """Analyzes a function for decorator patterns."""
        self.evidence, self.confidence = [], 0
        inner = DecoratorRules.find_inner_function(node)

        if inner and DecoratorRules.returns_inner(node, inner.name):
            self._add_evidence(
                f"Function contains and returns inner '{inner.name}'", 50
            )
            if DecoratorRules.has_wraps(inner):
                self._add_evidence("Uses @functools.wraps", 40)

        if self.confidence >= 50:
            res.append(
                {
                    "class": node.name,
                    "type": "function",
                    "confidence": min(self.confidence, 100),
                    "evidence": self.evidence,
                }
            )

    def _analyze_class(self, node: ast.ClassDef, res: List[Dict[str, Any]]) -> None:
        """Analyzes a class for decorator patterns."""
        self.evidence, self.confidence = [], 0
        if DecoratorRules.is_class_decorator(node):
            self._add_evidence("Class implements both __init__ and __call__", 60)

        if self.confidence >= 50:
            res.append(
                {
                    "class": node.name,
                    "type": "class",
                    "confidence": min(self.confidence, 100),
                    "evidence": self.evidence,
                }
            )


def detect_decorator(tree: ast.AST) -> List[Dict[str, Any]]:
    """Facade function to detect Decorator patterns in an AST.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of detected Decorator pattern instances.
    """
    detector = DecoratorDetector()
    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            detected = detector.detect(node)
            results.extend(detected)
    return results
