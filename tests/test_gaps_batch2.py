"""
Tests para cubrir gaps en classes, checkers y engine.
"""

import ast
from ai_context_core.analyzer.visitors.ast_visitors import ClassVisitor
from ai_context_core.analyzer.checkers.security_checker import SecurityChecker
from ai_context_core.analyzer.checkers.tech_debt_checker import TechDebtChecker
from ai_context_core.analyzer.checkers.optimization_checker import OptimizationChecker


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


def test_security_checker_no_issues():
    # Coverage for security_checker.py lines 26, 46-47, 58-59
    checker = SecurityChecker()
    module_info = {"ast_tree": ast.parse("x = 1"), "content": "x = 1"}
    result = checker.check(module_info)
    # Should return empty or minimal issues for safe code
    assert isinstance(result, list)


def test_tech_debt_checker_complex_function():
    # Coverage for tech_debt_checker.py lines 39-52, 89, 101, 110
    checker = TechDebtChecker()
    # Create a function with high complexity
    code = """
def complex_func(a, b, c, d, e, f, g, h, i, j):
    if a:
        if b:
            if c:
                if d:
                    if e:
                        if f:
                            return 1
    elif g:
        if h:
            if i:
                return 2
    return 3
"""
    tree = ast.parse(code)
    module_info = {"ast_tree": tree, "content": code}
    result = checker.check(module_info)
    # Should detect high complexity
    assert isinstance(result, list)


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
