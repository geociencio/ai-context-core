"""Design patterns detection module for ai-context-core.

Uses AST to identify common architectural patterns through a class-based detection system.
This module now acts as a facade for individual detectors located in `patterns_detectors`.
"""

import ast
from typing import Dict, List, Any
from .patterns_detectors.singleton import SingletonDetector
from .patterns_detectors.factory import FactoryDetector
from .patterns_detectors.observer import ObserverDetector
from .patterns_detectors.strategy import StrategyDetector
from .patterns_detectors.decorator import DecoratorDetector


class PatternsUnifiedVisitor(ast.NodeVisitor):
    """Orchestrates pattern detection in a single AST pass."""

    def __init__(self):
        self.detectors = {
            "Singleton": SingletonDetector(),
            "Factory": FactoryDetector(),
            "Observer": ObserverDetector(),
            "Strategy": StrategyDetector(),
            "Decorator": DecoratorDetector(),
        }
        self.results = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        for name, det in self.detectors.items():
            if hasattr(det, "visit"):
                det.visit(node)
                found = det.get_results(node)
            else:
                found = det.detect(node)

            if found:
                if name not in self.results:
                    self.results[name] = []
                self.results[name].extend(found)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Decorators or local patterns
        for name, det in self.detectors.items():
            if name == "Decorator":
                found = det.detect(node)
                if found:
                    if name not in self.results:
                        self.results[name] = []
                    self.results[name].extend(found)
        self.generic_visit(node)

    def visit_Module(self, node: ast.Module):
        # Module level patterns (e.g. PyQt signals at module level)
        det = self.detectors.get("Observer")
        if det:
            found = det.detect(node)
            if found:
                if "Observer" not in self.results:
                    self.results["Observer"] = []
                self.results["Observer"].extend(found)
        self.generic_visit(node)


def detect_patterns(tree: ast.AST) -> Dict[str, Any]:
    """Analyzes an AST to detect common design patterns using a unified visitor."""
    visitor = PatternsUnifiedVisitor()
    visitor.visit(tree)
    return visitor.results


# --- Legacy Compatibility Wrappers ---


def detect_singleton(tree: ast.AST) -> List[Dict[str, Any]]:
    det = SingletonDetector()
    res = []
    for node in ast.walk(tree):
        res.extend(det.detect(node))
    return res


def detect_factory(tree: ast.AST) -> List[Dict[str, Any]]:
    det = FactoryDetector()
    res = []
    for node in ast.walk(tree):
        res.extend(det.detect(node))
    return res


def detect_observer(tree: ast.AST) -> List[Dict[str, Any]]:
    det = ObserverDetector()
    res = []
    for node in ast.walk(tree):
        res.extend(det.detect(node))
    return res


def detect_strategy(tree: ast.AST) -> List[Dict[str, Any]]:
    det = StrategyDetector()
    res = []
    for node in ast.walk(tree):
        res.extend(det.detect(node))
    return res


def detect_decorator(tree: ast.AST) -> List[Dict[str, Any]]:
    det = DecoratorDetector()
    res = []
    for node in ast.walk(tree):
        res.extend(det.detect(node))
    return res
