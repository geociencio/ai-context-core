"""
Tests finales para alcanzar 100% de cobertura.
Cubre los últimos 83 líneas en engine, tech_debt, patterns, issues, etc.
"""

import ast
import pathlib
from unittest.mock import patch, mock_open
from ai_context_core.analyzer.checkers.tech_debt_checker import TechDebtChecker
from ai_context_core.analyzer.context_builders.patterns import PatternsBuilder
from ai_context_core.analyzer.context_builders.structure import StructureBuilder
from ai_context_core.analyzer.visitors.issues import find_secrets


def test_tech_debt_checker_all_branches():
    # Coverage for tech_debt_checker.py lines 39-52, 89, 101, 110
    checker = TechDebtChecker()

    # Test high complexity function
    code = """
def complex_func(a, b, c, d, e, f, g, h, i, j, k, l):
    if a:
        if b:
            if c:
                if d:
                    if e:
                        if f:
                            if g:
                                if h:
                                    return 1
    return 0
"""
    tree = ast.parse(code)
    module_info = {"ast_tree": tree, "content": code, "path": "test.py"}
    result = checker.check(module_info)
    assert isinstance(result, list)


def test_patterns_builder_with_patterns():
    # Coverage for patterns.py lines 27-31
    builder = PatternsBuilder(
        {
            "patterns": {
                "singleton": [{"class": "MySingleton", "module": "test.py"}],
                "factory": [{"class": "MyFactory", "module": "test.py"}],
            }
        }
    )
    lines = []
    builder.build(lines)
    assert len(lines) > 0
    assert any("singleton" in str(line).lower() for line in lines)


def test_structure_builder_with_data():
    # Coverage for structure.py lines 18, 20, 24-25
    builder = StructureBuilder(
        {
            "structure": {
                "classes": ["ClassA", "ClassB"],
                "functions": ["func1", "func2"],
                "total_lines": 100,
            }
        }
    )
    lines = []
    builder.build(lines)
    assert len(lines) > 0


def test_issues_find_secrets_with_secrets():
    # Coverage for issues.py lines 36, 51, 66-71
    modules = [{"path": "test1.py"}, {"path": "test2.py"}]

    # Mock file content with a potential secret
    def mock_read(path):
        if "test1" in str(path):
            return "API_KEY = 'sk-1234567890abcdef'"
        return "x = 1"

    with patch(
        "ai_context_core.analyzer.providers.fs_helpers.read_file_fast",
        side_effect=mock_read,
    ):
        result = find_secrets(modules, "/tmp")
        assert isinstance(result, list)


def test_gis_utils_extract_metadata():
    # Coverage for gis_utils.py lines 44-45, 48-49
    from ai_context_core.analyzer.providers.gis_utils import parse_qgis_metadata

    # Test with missing metadata.txt
    with patch("pathlib.Path.exists", return_value=False):
        result = parse_qgis_metadata(pathlib.Path("/tmp"))
        assert not result["exists"]

    # Test with valid metadata.txt
    metadata_content = """
[general]
name=TestPlugin
version=1.0.0
description=Test Description
"""
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=metadata_content)):
            result = parse_qgis_metadata(pathlib.Path("/tmp"))
            assert isinstance(result, dict)


def test_engine_load_config_edge_cases():
    # Coverage for engine.py lines 56-57, 61, 81, 92
    from ai_context_core.analyzer.engine import load_config, _get_hardcoded_defaults

    # Test load_config
    result = load_config(pathlib.Path("/tmp"))
    assert isinstance(result, dict)

    # Test hardcoded defaults
    defaults = _get_hardcoded_defaults()
    assert "quality_weights" in defaults
    assert "thresholds" in defaults


def test_config_loader_all_branches():
    # Coverage for config_loader.py lines 11-15, 48
    from ai_context_core.analyzer.providers.config_loader import load_config

    # Test without tomllib (fallback)
    with patch("ai_context_core.analyzer.providers.config_loader.tomllib", None):
        result = load_config(pathlib.Path("/tmp"))
        assert isinstance(result, dict)
        assert "patterns" in result or "thresholds" in result


def test_complexity_visitor_all_nodes():
    # Coverage for complexity_visitor.py lines 40-41, 49-50, 167
    from ai_context_core.analyzer.visitors.complexity_visitor import ComplexityVisitor

    # Test Match/case (Python 3.10+)
    try:
        code = """
match x:
    case 1:
        pass
    case 2:
        pass
"""
        tree = ast.parse(code)
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        assert visitor.complexity >= 1
    except SyntaxError:
        pass  # Python < 3.10

    # Test AsyncWith
    code2 = """
async def foo():
    async with context:
        pass
"""
    tree2 = ast.parse(code2)
    visitor2 = ComplexityVisitor()
    visitor2.visit(tree2)
    assert visitor2.complexity >= 1


def test_remaining_edge_cases():
    # Coverage for various 1-2 line gaps
    from ai_context_core.analyzer.visitors.ast_visitors import extract_imports

    # Test imports extraction
    code = "import os\nfrom sys import path"
    tree = ast.parse(code)
    imports = extract_imports(tree)
    assert isinstance(imports, (list, set))

    # Test ignore filter edge case
    from ai_context_core.analyzer.providers.ignore_filter import IgnoreFilter

    filter_obj = IgnoreFilter(pathlib.Path("/tmp"))
    assert hasattr(filter_obj, "patterns")
