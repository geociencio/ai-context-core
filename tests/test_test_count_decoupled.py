"""Regression tests: test-file counting must ignore .analyzerignore (A2)."""

from ai_context_core.analyzer.builders.calculator import calculate_project_metrics
from ai_context_core.analyzer.providers.fs_scanner import count_test_files, scan_project


def _write(path, content=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_count_test_files_ignores_analyzerignore(tmp_path):
    _write(tmp_path / "tests" / "test_foo.py")
    _write(tmp_path / "src" / "app.py")
    _write(tmp_path / ".analyzerignore", "tests/\n")

    # Analysis scan excludes tests/, so its scope count is zero...
    scan = scan_project(tmp_path, [])
    assert scan.test_files_count == 0
    # ...but the decoupled counter still reports the real test suite.
    assert count_test_files(tmp_path) == 1


def test_count_test_files_returns_none_for_missing_path(tmp_path):
    assert count_test_files(tmp_path / "does-not-exist") is None


def test_ignored_tests_do_not_penalize_score(tmp_path):
    _write(tmp_path / "tests" / "test_foo.py")
    _write(tmp_path / ".analyzerignore", "tests/\n")

    modules = [
        {
            "path": "app.py",
            "sloc": 100,
            "lines": 120,
            "functions": [],
            "classes": [],
            "complexity": 1,
            "maintenance_index": 90.0,
        }
    ]

    count = count_test_files(tmp_path)
    with_tests = calculate_project_metrics(modules, [], count, {})["quality_score"]
    without_tests = calculate_project_metrics(modules, [], 0, {})["quality_score"]

    assert with_tests == 100.0
    assert with_tests > without_tests
