import ast
import pytest
from ai_context_core.analyzer.visitors.insecure_calls import (
    InsecureCallsChecker,
)
from ai_context_core.analyzer.security_checkers.base import BaseSecurityChecker
from ai_context_core.analyzer.patterns_detectors.observer_rules import (
    analyze_class_body,
)


def test_pickle_usage_insecure_calls():
    checker = InsecureCallsChecker()
    issues = []
    # Test line 49 of insecure_calls.py
    code = "import pickle; pickle.loads(data)"
    tree = ast.parse(code)
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert any("pickle.loads" in i["pattern"] for i in issues)


def test_base_security_checker_abstract():
    checker = BaseSecurityChecker()
    # Test line 25 of base.py
    with pytest.raises(NotImplementedError):
        checker.check(ast.parse("pass"), [])


def test_observer_signal_connection_coverage():
    # Test class_analyzer.py line 36
    results = []

    def add_evidence(msg, confidence):
        results.append(msg)

    code = """
class MyEmitter:
    def __init__(self):
        self.sig.connect(self.handler)
"""
    tree = ast.parse(code)
    cls = tree.body[0]
    analyze_class_body(cls, add_evidence)
    assert any("Signal connection detected" in m for m in results)


def test_observer_collection_init_coverage():
    # Test collections.py line 24 (False case already covered, need True)
    from ai_context_core.analyzer.patterns_detectors.observer_rules import (
        check_init_assign,
    )

    # attr based
    node = ast.parse("self.observers = []").body[0]
    assert check_init_assign(node) is True

    # non-attr target
    node = ast.parse("observers = []").body[0]
    assert check_init_assign(node) is False


def test_observer_iteration_coverage():
    # Test collections.py line 34 (False case already covered, need True)
    from ai_context_core.analyzer.patterns_detectors.observer_rules import (
        check_iteration,
    )

    code = "for o in self.observers: o.update()"
    tree = ast.parse(code)
    assert check_iteration(tree) is True

    code = "for i in range(10): pass"
    tree = ast.parse(code)
    assert check_iteration(tree) is False
