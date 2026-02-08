import ast
from unittest.mock import MagicMock, PropertyMock
from ai_context_core.analyzer.visitors.ast_entry_points import (
    is_entry_point,
    has_main_guard,
    EntryPointVisitor,
)
from ai_context_core.analyzer.entry_point_detectors.framework_rules import DecoratorRule


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


def test_entry_point_assign_frameworks():
    # Django
    assert (
        is_entry_point(ast.parse("application = get_wsgi_application()"))["type"]
        == "django_app"
    )
    assert is_entry_point(ast.parse("urlpatterns = []"))["type"] == "django_urls"
    assert is_entry_point(ast.parse("INSTALLED_APPS = []"))["type"] == "django_settings"
    # Flask
    assert is_entry_point(ast.parse("app = Flask(__name__)"))["type"] == "flask_app"
    # FastAPI
    assert is_entry_point(ast.parse("app = FastAPI()"))["type"] == "fastapi_app"


def test_decorator_rules_coverage():
    # Coverage for DecoratorRule lines 12-17 and types
    rule = DecoratorRule()
    # Not call/attr/name
    assert rule.check(ast.BinOp()) is None
    # Call but not attribute
    # @deco -> deco is Name
    assert (
        rule.check(ast.parse("@deco\ndef f(): pass").body[0].decorator_list[0]) is None
    )

    # Click
    click_deco = ast.parse("@click.command()\ndef f(): pass").body[0].decorator_list[0]
    assert rule.check(click_deco) == "click_cli"

    # Flask route
    flask_deco = ast.parse("@app.route('/')\ndef f(): pass").body[0].decorator_list[0]
    assert rule.check(flask_deco) == "flask_app"

    # FastAPI
    fastapi_deco = ast.parse("@app.get('/')\ndef f(): pass").body[0].decorator_list[0]
    assert rule.check(fastapi_deco) == "fastapi_app"
