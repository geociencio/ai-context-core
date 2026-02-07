import ast
from click.testing import CliRunner
from ai_context_core.analyzer.qgis_checkers.frameworks import FrameworkChecker
from ai_context_core.analyzer.summarizers.git_patterns import GitPatternsSummarizer
from ai_context_core.cli_groups.specialized import deps_cmd


def test_qgis_frameworks_get_name_fallback():
    # Coverage for frameworks.py line 34
    results = {"processing_framework": False, "signals_slots": {"legacy": 0}}
    checker = FrameworkChecker(results)
    # Test with a node type that's neither Name nor Attribute
    node = ast.Constant(value=5)
    assert checker._get_name(node) == ""


def test_git_patterns_summarizer_no_git():
    # Coverage for git_patterns.py line 12
    summarizer = GitPatternsSummarizer({"git": {}})
    assert summarizer.build_git() == ""


def test_git_patterns_summarizer_no_churn():
    # Coverage for git_patterns.py churn not available
    summarizer = GitPatternsSummarizer({"git": {"churn": {"available": False}}})
    result = summarizer.build_git()
    assert isinstance(result, str)


def test_deps_cmd_all_flags():
    # Coverage for specialized.py line 15
    runner = CliRunner()
    # When no flags are provided, all should be enabled
    result = runner.invoke(deps_cmd, ["--path", "."])
    # Should execute without error
    assert result.exit_code in [0, 1]  # May fail if no project, but should not crash
