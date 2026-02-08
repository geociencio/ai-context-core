"""Strategy pattern detector implementation."""

import ast
from typing import Dict, List, Any
from .pattern_base import PatternDetector


from .strategy_rules import StrategyRules


class StrategyDetector(PatternDetector):
    """Detects Strategy pattern implementations.

    Delegates rule checking to StrategyRules to keep complexity low.
    """

    def detect(self, node: ast.AST) -> List[Dict[str, Any]]:
        """Detect Strategy pattern implementations in a node.

        Args:
            node: The AST node to analyze.

        Returns:
            List of detected strategy instances.

        """
        if not isinstance(node, ast.ClassDef):
            return []

        self.evidence, self.confidence = [], 0
        has_inj = self._check_for_injection(node)

        if has_inj:
            self._check_for_calls(node)

        if self.confidence >= 50:
            return [
                {
                    "class": node.name,
                    "confidence": min(self.confidence, 100),
                    "evidence": self.evidence,
                }
            ]
        return []

    def _check_for_injection(self, node: ast.ClassDef) -> bool:
        """Check class methods for strategy injection."""
        has_inj = False
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and (
                item.name == "__init__" or "set_" in item.name
            ):
                arg_name = StrategyRules.check_injection(item)
                if arg_name:
                    has_inj = True
                    self._add_evidence(
                        f"Injection detected in '{item.name}' via '{arg_name}'", 30
                    )
        return has_inj

    def _check_for_calls(self, node: ast.ClassDef) -> None:
        """Check class methods for calls to injected strategies."""
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name not in (
                "__init__",
                "set_",
            ):
                call_str = StrategyRules.detect_strategy_call(item)
                if call_str:
                    self._add_evidence(
                        f"Strategy call in '{item.name}': {call_str}()", 40
                    )


def detect_strategy(tree: ast.AST) -> List[Dict[str, Any]]:
    """Facade function to detect Strategy patterns in an AST.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of detected Strategy pattern instances.

    """
    detector = StrategyDetector()
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            detected = detector.detect(node)
            results.extend(detected)
    return results
