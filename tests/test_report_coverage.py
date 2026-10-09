from ai_context_core.cli.commands.report import (
    _show_patterns,
    _show_security,
    _show_recommendations,
)
from unittest.mock import patch


def test_report_show_patterns_empty():
    # Coverage for report.py line 29
    with patch("click.echo") as mock_echo:
        _show_patterns({"patterns": {}})
        # Should print "No patterns detected."
        mock_echo.assert_called_with("No patterns detected.")


def test_report_show_security_empty():
    # Coverage for report.py line 42
    with patch("click.echo") as mock_echo:
        _show_security({"security": []})
        # Should print "No issues found."
        mock_echo.assert_called_with("No issues found.")


def test_report_show_recommendations_empty():
    # Coverage for report.py line 55
    with patch("click.echo") as mock_echo:
        _show_recommendations({"optimizations": []})
        # Should print "No recommendations."
        mock_echo.assert_called_with("No recommendations.")


def test_ai_context_generator_sections():
    from ai_context_core.analyzer.builders.ai_context_generator import AIContextGenerator

    analyses = {
        "structure": {"tree": "src/", "modules_count": 1, "file_types": {}, "size_stats": {}},
        "metrics": {},
        "dependencies": {},
        "git": {},
        "patterns": {},
        "qgis_compliance": {},
        "entry_points": [],
        "manual_notes": "",
    }
    gen = AIContextGenerator(analyses, "Test", config={"context": {"sections": ["structure"]}})
    content = gen.build()
    assert "PROJECT STRUCTURE" in content
    assert "COMPLEXITY AND METRICS" not in content


def test_detect_unused_imports_skips_future():
    import ast

    from ai_context_core.analyzer.visitors.imports_visitor import detect_unused_imports

    tree = ast.parse("from __future__ import annotations\nimport sys\n")
    unused = detect_unused_imports(tree)
    assert "sys" in unused
    assert not any(u.startswith("__future__") for u in unused)
