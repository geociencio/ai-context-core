import ast
from ai_context_core.analyzer.visitors.ast_metrics import (
    calculate_type_hint_coverage,
    TypeHintVisitor,
)


def test_type_hint_coverage_edge_cases():
    # Function with no return type hint
    code_no_ret = "def f(a: int): pass"
    assert calculate_type_hint_coverage(ast.parse(code_no_ret))["coverage"] == 0.0

    # Function with untyped args
    code_untyped_arg = "def f(a) -> int: pass"
    assert calculate_type_hint_coverage(ast.parse(code_untyped_arg))["coverage"] == 0.0

    # Mixed typed/untyped args
    code_mixed = "def f(a: int, b) -> int: pass"
    assert calculate_type_hint_coverage(ast.parse(code_mixed))["coverage"] == 0.0

    # All typed including return
    code_all = "def f(a: int) -> int: pass"
    assert calculate_type_hint_coverage(ast.parse(code_all))["coverage"] == 100.0


def test_type_hint_visitor_init():
    v = TypeHintVisitor()
    assert v.total_functions == 0
    assert v.typed_functions == 0
