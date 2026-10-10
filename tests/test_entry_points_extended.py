import ast
from unittest.mock import MagicMock, PropertyMock
from ai_context_core.analyzer.visitors.ast_entry_points import (
    is_entry_point,
    has_main_guard,
    EntryPointVisitor,
)


def test_entry_point_visitor_assign_early_return():
    # Coverage for visit_Assign line 45 (return if already is_entry_point)
    code = "app = Flask(__name__)"
    visitor = EntryPointVisitor()
    visitor.result = {"is_entry_point": True, "type": "existing"}
    visitor.visit(ast.parse(code))
    assert visitor.result["type"] == "existing"


def test_main_guard_exception_path():
    # Coverage for _is_main_guard line 68-69 (try-except)
    node = MagicMock(spec=ast.If)
    # Accessing test raises exception
    type(node).test = PropertyMock(side_effect=Exception("Simulated error"))

    visitor = EntryPointVisitor()
    assert visitor._is_main_guard(node) is False


def test_has_main_guard_logic():
    assert has_main_guard(ast.parse('if __name__ == "__main__": pass')) is True
    assert has_main_guard(ast.parse("x = 1")) is False


def test_entry_point_main_guard_detection():
    assert is_entry_point(ast.parse('if __name__ == "__main__": pass'))["type"] == "main_guard"
    assert is_entry_point(ast.parse("app = Flask(__name__)"))["type"] is None
