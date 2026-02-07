import ast
import pytest
from ai_context_core.analyzer.patterns_detectors.base import PatternDetector
from ai_context_core.analyzer.patterns_detectors.decorator_rules import DecoratorRules


def test_pattern_detector_no_visit():
    # Test base.py line 26
    det = PatternDetector()
    with pytest.raises(NotImplementedError):
        det.detect(ast.parse("pass"))


def test_decorator_rules_returns_inner_false():
    # Test decorator_rules.py line 47
    code = """
def outer():
    def inner(): pass
    return None
"""
    tree = ast.parse(code)
    func = tree.body[0]
    assert DecoratorRules.returns_inner(func, "inner") is False


def test_decorator_rules_has_wraps_attr():
    # Test decorator_rules.py line 61-62 (attr case)
    code = """
def dec(f):
    @functools.wraps(f)
    def w(): pass
    return w
"""
    tree = ast.parse(code)
    inner = tree.body[0].body[0]
    assert DecoratorRules.has_wraps(inner) is True
