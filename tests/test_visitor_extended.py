import ast
from ai_context_core.analyzer.patterns_components.visitor import PatternsUnifiedVisitor


def test_visitor_decorator_detection():
    # Test visit_FunctionDef branch (lines 47-49)
    code = """
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def decorated():
    pass
"""
    tree = ast.parse(code)
    visitor = PatternsUnifiedVisitor()
    visitor.visit(tree)

    assert "Decorator" in visitor.results
    assert len(visitor.results["Decorator"]) > 0


def test_visitor_module_observer_detection():
    # Test visit_Module branch (lines 57-59)
    # Observer detector needs >= 50 confidence.
    # Each signal adds 20. So 3 signals = 60.
    code = """
import PyQt6.QtCore
sig1 = PyQt6.QtCore.pyqtSignal()
sig2 = PyQt6.QtCore.pyqtSignal()
sig3 = PyQt6.QtCore.pyqtSignal()
"""
    tree = ast.parse(code)
    visitor = PatternsUnifiedVisitor()
    visitor.visit(tree)

    assert "Observer" in visitor.results
    assert visitor.results["Observer"][0]["confidence"] >= 50
