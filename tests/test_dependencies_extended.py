import ast
import pathlib
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.builders.dependencies import (
    analyze_dependencies,
    DependencyAnalyzer,
    STDLIB_MODULES,
)
from ai_context_core.analyzer.builders.algorithms import (
    CycleDetector,
    GraphMetricsCalculator,
)
from ai_context_core.analyzer.builders.builder import ImportGraphBuilder
from ai_context_core.analyzer.builders.builder_components import resolve_import
from ai_context_core.analyzer.builders.classifier import classify_imports
from ai_context_core.analyzer.builders.parser import parse_dependency_files
from ai_context_core.analyzer.visitors.imports_visitor import extract_imports, get_package


def test_analyze_dependencies_cycle_exception():
    # Coverage for dependencies.py line 124-125
    with patch(
        "ai_context_core.analyzer.builders.dependencies.CycleDetector.find_cycles",
        side_effect=Exception("Cycle error"),
    ):
        res = analyze_dependencies([], pathlib.Path("/tmp"), MagicMock())
        assert res["circular_dependencies"] == []


def test_analyze_dependencies_metrics_exception():
    # Coverage for dependencies.py line 142-143
    with patch(
        "ai_context_core.analyzer.builders.dependencies.GraphMetricsCalculator.count_edges",
        side_effect=Exception("Metrics error"),
    ):
        with patch("ai_context_core.analyzer.builders.dependencies.logger") as mock_log:
            res = analyze_dependencies([], pathlib.Path("/tmp"), MagicMock())
            assert res["graph_metrics"] == {}
            mock_log.exception.assert_called()


def test_dependency_graph_metrics():
    graph = {"a": {"b"}, "b": set()}
    calc = GraphMetricsCalculator(graph)
    assert calc.count_edges() == 1
    assert CycleDetector(graph).find_cycles() == []
    assert calc.count_connected_components() == 1
    coupling = calc.calculate_coupling_metrics()
    assert "a" in coupling


def test_dependency_analyzer_legacy():
    # Coverage for DependencyAnalyzer class (lines 223-248)
    analyzer = DependencyAnalyzer(pathlib.Path("/tmp"))
    with patch(
        "ai_context_core.analyzer.builders.dependencies.analyze_dependencies"
    ) as mock_analyze:
        analyzer.build_graph([])
        mock_analyze.assert_called()


def test_classify_imports_full_coverage():
    # Case where an import is both internal and external
    res = classify_imports({"os", "my_mod"}, STDLIB_MODULES, known_internal={"my_mod"})
    assert "os" in res["external"]
    assert "my_mod" in res["internal"]


def test_parse_dependency_files_components():
    def mock_read(p):
        if p.name == "requirements.txt":
            return "flask\nrequests"
        if p.name == "pyproject.toml":
            return '[project]\nname="test"'
        return ""

    with patch("pathlib.Path.exists", return_value=True):
        res = parse_dependency_files(pathlib.Path("/tmp"), mock_read)
        assert "requirements.txt" in res
        assert "pyproject.toml" in res


def test_resolve_import_strips_package_prefix():
    import_map = {"core.x": "core/x.py"}
    top_level = {"core"}
    assert resolve_import("sec_interp.core.x", import_map, top_level) == "core/x.py"
    assert resolve_import("core.x", import_map, top_level) == "core/x.py"
    assert resolve_import("os.path", import_map, top_level) is None


def test_import_graph_builder_prefixed_import():
    modules = [
        {"path": "core/x.py", "imports": ["sec_interp.core.y"]},
        {"path": "core/y.py", "imports": []},
    ]
    graph = ImportGraphBuilder(modules).build()
    assert "core/y.py" in graph["core/x.py"]


def test_relative_import_resolution():
    tree = ast.parse("from . import sibling\nfrom ..parent import thing\n")
    imports = extract_imports(tree, package="pkg.sub")
    assert "pkg.sub.sibling" in imports
    assert "pkg.parent.thing" in imports


def test_get_package():
    assert get_package("core/x.py") == "core"
    assert get_package("core/__init__.py") == "core"
    assert get_package("plugin.py") == ""
    assert get_package("src/ai_context_core/engine.py") == "ai_context_core"
