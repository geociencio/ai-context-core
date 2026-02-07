"""Unified patterns visitor for one-pass detection."""

import ast
from ..patterns_detectors.singleton import SingletonDetector
from ..patterns_detectors.factory import FactoryDetector
from ..patterns_detectors.observer import ObserverDetector
from ..patterns_detectors.strategy import StrategyDetector
from ..patterns_detectors.decorator import DecoratorDetector

class PatternsUnifiedVisitor(ast.NodeVisitor):
    """Orchestrates pattern detection in a single AST pass."""

    def __init__(self):
        """Initialize the unified visitor with selective detectors."""
        self.detectors = {
            "Singleton": SingletonDetector(),
            "Factory": FactoryDetector(),
            "Observer": ObserverDetector(),
            "Strategy": StrategyDetector(),
            "Decorator": DecoratorDetector(),
        }
        self.results = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits a class definition to detect patterns."""
        for name, det in self.detectors.items():
            found = det.get_results(node) if hasattr(det, "visit") else det.detect(node)
            if found:
                if name not in self.results:
                    self.results[name] = []
                self.results[name].extend(found)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits a function definition to detect patterns."""
        self.generic_visit(node)
        det = self.detectors.get("Decorator")
        if det:
            found = det.detect(node)
            if found:
                if "Decorator" not in self.results:
                    self.results["Decorator"] = []
                self.results["Decorator"].extend(found)

    def visit_Module(self, node: ast.Module):
        """Visits a module to detect global patterns."""
        det = self.detectors.get("Observer")
        if det:
            found = det.detect(node)
            if found:
                if "Observer" not in self.results:
                    self.results["Observer"] = []
                self.results["Observer"].extend(found)
        self.generic_visit(node)
