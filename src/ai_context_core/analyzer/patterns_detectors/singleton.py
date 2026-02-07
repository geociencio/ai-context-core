"""Singleton pattern detector implementation."""

import ast
from .base import PatternDetector


from .singleton_rules import check_singleton_item


class SingletonDetector(PatternDetector):
    """Detects Singleton pattern implementations.

    Delegates rule checking to specialized components.
    """

    def visit(self, node: ast.AST):
        """Analyze a node to find Singleton pattern evidence.

        Args:
            node: The AST node to analyze.

        """
        self.evidence, self.confidence = [], 0
        if not isinstance(node, ast.ClassDef):
            return

        for item in node.body:
            check_singleton_item(item, self._add_evidence)


def detect_singleton(tree: ast.AST):
    """Facade function to detect Singleton patterns in an AST.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of detected Singleton pattern instances with confidence >= 50.

    """
    detector = SingletonDetector()
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            detector.visit(node)
            # Only report patterns with confidence >= 50
            if detector.evidence and detector.confidence >= 50:
                results.append(
                    {
                        "class": node.name,
                        "evidence": detector.evidence,
                        "confidence": detector.confidence,
                    }
                )
    return results
