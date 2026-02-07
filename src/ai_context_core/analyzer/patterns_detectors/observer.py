"""Observer pattern detector implementation."""

import ast
from typing import Dict, List, Any
from .base import PatternDetector

from .observer_components import detect_signals, analyze_class_body


class ObserverDetector(PatternDetector):
    """Detects Observer pattern implementations.

    Delegates analysis to specialized components to maintain extremely low complexity.
    """

    def detect(self, node: ast.AST) -> List[Dict[str, Any]]:
        """Detects Observer pattern implementations in a node.

        Args:
            node: The AST node to analyze.

        Returns:
            List of detected observer instances.
        """
        self.evidence, self.confidence = [], 0
        name = getattr(node, "name", "Module")

        if isinstance(node, ast.ClassDef):
            analyze_class_body(node, self._add_evidence)

        if isinstance(node, (ast.ClassDef, ast.Module)):
            signals = detect_signals(node)
            if signals > 0:
                self._add_evidence(
                    f"Detected {signals} signals (PyQt/Signals)", signals * 20
                )

        if self.confidence >= 50:
            return [
                {
                    "class": name,
                    "confidence": min(self.confidence, 100),
                    "evidence": self.evidence,
                }
            ]
        return []


def detect_observer(tree: ast.AST) -> List[Dict[str, Any]]:
    """Facade function to detect Observer patterns in an AST.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of detected Observer pattern instances.
    """
    detector = ObserverDetector()
    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.Module)):
            detected = detector.detect(node)
            results.extend(detected)
    return results
