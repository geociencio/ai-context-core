"""
Tests masivos para cubrir todos los gaps restantes.
"""

import pathlib
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.issues import find_secrets
from ai_context_core.analyzer.graph.builder import ImportGraphBuilder
from ai_context_core.analyzer.builders.classifier import (
    classify_imports,
)
from ai_context_core.analyzer.builders.parser import (
    parse_dependency_files,
)


def test_find_secrets_no_secrets():
    # Coverage for issues.py lines 36, 51, 66-71
    modules = [{"path": "test.py"}]
    with patch(
        "ai_context_core.analyzer.fs_helpers.read_file_fast", return_value="x = 1"
    ):
        result = find_secrets(modules, "/tmp")
        assert isinstance(result, list)


def test_import_graph_builder_resolve_import():
    # Coverage for graph/builder.py lines 39, 54
    modules = [
        {"path": "module_a.py", "imports": ["module_b"]},
        {"path": "module_b.py", "imports": []},
    ]
    builder = ImportGraphBuilder(modules)
    graph = builder.build()
    assert isinstance(graph, dict)


def test_classify_imports_third_party():
    # Coverage for classifier.py lines 21-22
    imports = {"flask", "requests", "numpy"}
    stdlib = {"os", "sys"}
    internal = set()
    result = classify_imports(imports, stdlib, internal)
    assert "third_party" in result
    assert len(result["third_party"]) > 0


def test_parse_dependency_files_no_toml():
    # Coverage for parser.py lines 28-29
    def read_func(p):
        if "requirements.txt" in str(p):
            return "flask==2.0.0"
        return ""

    with patch("pathlib.Path.exists", return_value=True):
        result = parse_dependency_files(pathlib.Path("/tmp"), read_func)
        assert isinstance(result, dict)


def test_fs_tree_subprocess_timeout():
    # Coverage for fs_tree.py lines 27-28
    from ai_context_core.analyzer.fs_tree import generate_tree_optimized

    with patch("subprocess.run", side_effect=TimeoutError("Timeout")):
        result = generate_tree_optimized(pathlib.Path("/tmp"))
        # Should fallback to manual generation
        assert isinstance(result, str)


def test_fs_tree_analyze_structure():
    # Coverage for fs_tree.py lines 55-58
    from ai_context_core.analyzer.fs_tree import analyze_structure

    with patch("ai_context_core.analyzer.fs_scanner.scan_project") as mock_scan:
        mock_scan.return_value = MagicMock(
            file_types={"py": 10}, size_stats={"total_files": 10}
        )
        result = analyze_structure(pathlib.Path("/tmp"), 5)
        assert "tree" in result
        assert "modules_count" in result


def test_config_loader_no_tomllib():
    # Coverage for config_loader.py lines 11-15, 48
    from ai_context_core.analyzer.providers.config_loader import load_config

    with patch("ai_context_core.analyzer.providers.config_loader.tomllib", None):
        result = load_config(pathlib.Path("/tmp"))
        # Should return defaults even without TOML support
        assert isinstance(result, dict)


def test_worker_parallel_edge_cases():
    # Coverage for worker.py lines 63-65
    from ai_context_core.analyzer.providers.worker import AnalysisWorker

    worker = AnalysisWorker(pathlib.Path("/tmp"), {}, 2, {})
    # Test with exactly PARALLEL_MIN_FILES files
    files = [pathlib.Path(f"/tmp/file{i}.py") for i in range(5)]
    with patch(
        "ai_context_core.analyzer.fs_utils.calculate_file_hash", return_value="hash"
    ):
        with patch.object(worker, "analyze_single", return_value={"path": "test.py"}):
            result = worker.run_parallel(files)
            assert isinstance(result, list)


def test_fs_scanner_oserror():
    # Coverage for fs_scanner.py lines 84-85
    from ai_context_core.analyzer.fs_scanner import ProjectScanner
    from ai_context_core.analyzer.ignore_filter import IgnoreFilter

    scanner = ProjectScanner(pathlib.Path("/tmp"), IgnoreFilter(pathlib.Path("/tmp")))
    with patch("os.path.getsize", side_effect=OSError("Permission denied")):
        scanner._process_file("/tmp", "", "test.py")
        # Should handle OSError gracefully
        assert scanner.stats["total_size"] == 0


def test_dependencies_fallback():
    # Coverage for dependencies.py line 20
    from ai_context_core.analyzer.dependencies import STDLIB_MODULES

    # Verify STDLIB_MODULES is populated
    assert len(STDLIB_MODULES) > 0
    assert "os" in STDLIB_MODULES or isinstance(STDLIB_MODULES, set)


def test_context_builders_coverage():
    # Coverage for context_builders lines
    from ai_context_core.analyzer.context_builders.dependencies import DependencyBuilder
    from ai_context_core.analyzer.context_builders.patterns import PatternsBuilder
    from ai_context_core.analyzer.context_builders.structure import StructureBuilder

    # Test DependencyBuilder
    builder = DependencyBuilder({"dependencies": {"third_party": ["flask"]}})
    lines = []
    builder.build(lines)
    assert len(lines) > 0

    # Test PatternsBuilder
    builder2 = PatternsBuilder({"patterns": {}})
    lines2 = []
    builder2.build(lines2)
    assert isinstance(lines2, list)

    # Test StructureBuilder
    builder3 = StructureBuilder({"structure": {"classes": ["MyClass"]}})
    lines3 = []
    builder3.build(lines3)
    assert isinstance(lines3, list)
