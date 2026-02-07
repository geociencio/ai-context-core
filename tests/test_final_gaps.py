import ast
import pytest
from ai_context_core.analyzer.patterns_detectors.singleton_components.method_rules import (
    check_singleton_method,
)
from ai_context_core.analyzer.qgis_checkers.base import BaseQGISChecker
from ai_context_core.analyzer.summarizers.base import BaseSummarizer


def test_singleton_method_attr_decorator_coverage():
    # Test method_rules.py line 25: @foo.classmethod
    results = []

    def add_evidence(msg, conf):
        results.append(msg)

    code = """
class MySingleton:
    @some_mod.classmethod
    def get_instance(cls): pass
"""
    tree = ast.parse(code)
    func = tree.body[0].body[0]
    check_singleton_method(func, add_evidence)
    assert any("Static/Class method" in m for m in results)


def test_base_qgis_checker_abstract():
    # Test base.py line 20
    checker = BaseQGISChecker({})
    with pytest.raises(NotImplementedError):
        checker.visit(ast.parse("pass"))


def test_base_qgis_checker_extra_parts_returns():
    # Test base.py line 49 (node.returns)
    class MockVisitor(ast.NodeVisitor):
        def __init__(self):
            self.visited_returns = False

        def visit_Name(self, node):
            if node.id == "int":
                self.visited_returns = True

    checker = BaseQGISChecker({})
    visitor = MockVisitor()

    code = "def foo() -> int: pass"
    tree = ast.parse(code)
    func = tree.body[0]

    checker.generic_visit_with_docstring_skip(visitor, func)
    assert visitor.visited_returns is True


def test_base_summarizer_abstract():
    # Test summarizers/base.py line 23
    summarizer = BaseSummarizer({})
    with pytest.raises(NotImplementedError):
        summarizer.build()
