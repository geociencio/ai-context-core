import pathlib
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.dependencies import (
    analyze_dependencies,
    find_simple_cycles,
    count_edges,
    count_connected_components,
    calculate_coupling_metrics,
    DependencyAnalyzer,
)


def test_analyze_dependencies_cycle_exception():
    # Coverage for dependencies.py line 124-125
    with patch(
        "ai_context_core.analyzer.graph_engine.CycleDetector.find_cycles",
        side_effect=Exception("Cycle error"),
    ):
        res = analyze_dependencies([], pathlib.Path("/tmp"), MagicMock())
        assert res["circular_dependencies"] == []


def test_analyze_dependencies_metrics_exception():
    # Coverage for dependencies.py line 142-143
    with patch(
        "ai_context_core.analyzer.graph_engine.GraphMetricsCalculator.count_edges",
        side_effect=Exception("Metrics error"),
    ):
        with patch("ai_context_core.analyzer.builders.dependencies.logger") as mock_log:
            res = analyze_dependencies([], pathlib.Path("/tmp"), MagicMock())
            assert res["graph_metrics"] == {}
            mock_log.exception.assert_called()


def test_dependency_legacy_wrappers():
    # Coverage for lines 188-220
    graph = {"a": {"b"}, "b": set()}
    assert count_edges(graph) == 1
    assert find_simple_cycles(graph) == []
    assert count_connected_components(graph) == 1
    coupling = calculate_coupling_metrics(graph)
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
    # Coverage for dependency_analyser_components/classifier.py (via dependencies.py)
    from ai_context_core.analyzer.dependencies import _classify_imports, STDLIB_MODULES

    # Test case where import is both internal and external (should favor internal usually, or depends on implementation)
    res = _classify_imports({"os", "my_mod"}, STDLIB_MODULES, known_internal={"my_mod"})
    # 'os' should be in 'stdlib' or 'external' depending on classifier implementation
    # Let's see what keys it returns
    assert "os" in res["external"]
    assert "my_mod" in res["internal"]


def test_parse_dependency_files_components():
    # Coverage for parser.py
    from ai_context_core.analyzer.dependencies import _parse_dependency_files

    def mock_read(p):
        if p.name == "requirements.txt":
            return "flask\nrequests"
        if p.name == "pyproject.toml":
            return '[project]\nname="test"'
        return ""

    with patch("pathlib.Path.exists", return_value=True):
        res = _parse_dependency_files(pathlib.Path("/tmp"), mock_read)
        assert "requirements.txt" in res
        assert "pyproject.toml" in res
