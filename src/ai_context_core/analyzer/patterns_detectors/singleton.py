"""Singleton pattern detector implementation."""

import ast
from ..constants import PATTERN_DETECTION_CONFIDENCE_HIGH
from .base import PatternDetector


from .singleton_components import check_singleton_item

class SingletonDetector(PatternDetector):
    """Detects Singleton pattern implementations.
    
    Delegates rule checking to specialized components.
    """

    def visit(self, node: ast.AST):
        """Analyzes a node to find Singleton pattern evidence.

        Args:
            node: The AST node to analyze.
        """
        self.evidence, self.confidence = [], 0
        if not isinstance(node, ast.ClassDef):
            return
            
        for item in node.body:
            check_singleton_item(item, self._add_evidence)
