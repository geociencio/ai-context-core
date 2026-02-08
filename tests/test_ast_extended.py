import ast
from ai_context_core.analyzer.visitors.ast_utils import extract_base_name
from ai_context_core.analyzer.visitors.ast_metrics import (
    calculate_type_hint_coverage,
    HalsteadVisitor,
    TypeHintVisitor,
)


def test_extract_base_name_variants():
    # Attribute
    node_attr = ast.Attribute(
        value=ast.Name(id="mod", ctx=ast.Load()), attr="Base", ctx=ast.Load()
    )
    assert extract_base_name(node_attr) == "Base"

    # Call
    node_call = ast.Call(
        func=ast.Name(id="MyClass", ctx=ast.Load()), args=[], keywords=[]
    )
    assert extract_base_name(node_call) == "MyClass"

    # Unknown
    assert extract_base_name(ast.Constant(value=1)) == "Unknown"


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


def test_halstead_visitor_generic():
    # Coverage for HalsteadVisitor line 83-89
    visitor = HalsteadVisitor()
    tree = ast.parse("x = 1 + 2")
    visitor.visit(tree)
    # 1 (+) operator
    assert "Add" in visitor.operators
    # x, 1, 2 operands
    assert "x" in visitor.operands
    assert "1" in visitor.operands
    assert "2" in visitor.operands

    # Test unknown node type in Halstead (should still visit children)
    # Using a Module node (which is not in OPERATORS usually, but we check for specific roles)
    # Actually OPERATORS has mostly specific types.
    # Constant coverage
    node_const = ast.Constant(value="hello")
    visitor.visit(node_const)
    assert "hello" in visitor.operands


def test_type_hint_visitor_init():
    v = TypeHintVisitor()
    assert v.total_functions == 0
    assert v.typed_functions == 0
