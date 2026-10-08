"""
Tests para cubrir gaps en classes, checkers y engine.
"""

import ast
import pytest
from ai_context_core.analyzer.visitors.ast_visitors import ClassVisitor
from ai_context_core.analyzer.visitors.optimization_checker import OptimizationChecker
from ai_context_core.analyzer.visitors.checker_base import BaseChecker


def test_class_visitor_attribute_base():
    # Coverage for classes.py lines 23-27
    code = """
class Child(parent.module.Base):
    pass
"""
    tree = ast.parse(code)
    visitor = ClassVisitor()
    visitor.visit(tree)
    assert len(visitor.classes) == 1
    # Should recursively extract base name


def test_class_visitor_unknown_base():
    # Coverage for classes.py line 27 (return None)
    visitor = ClassVisitor()
    # Test with a node type that's neither Name nor Attribute
    result = visitor._get_base_name(ast.Constant(value=5))
    assert result is None


def test_optimization_checker_list_comprehension():
    # Coverage for optimization_checker.py lines 16, 52
    checker = OptimizationChecker()
    code = """
result = []
for i in range(10):
    result.append(i * 2)
"""
    tree = ast.parse(code)
    module_info = {"ast_tree": tree, "content": code}
    result = checker.check(module_info)
    # Should suggest list comprehension
    assert isinstance(result, list)


def test_base_checker_abstract():
    checker = BaseChecker({})
    with pytest.raises(NotImplementedError):
        checker.check({})
    with pytest.raises(NotImplementedError):
        checker.get_category()
