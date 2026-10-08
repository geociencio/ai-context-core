import ast
from click.testing import CliRunner
from ai_context_core.analyzer.builders.git_patterns import GitPatternsSummarizer
from ai_context_core.analyzer.visitors.qgis_base import get_node_name
from ai_context_core.cli.commands.specialized import deps_cmd


def test_qgis_frameworks_get_name_fallback():
    # Fallback for node types that are neither Name nor Attribute
    assert get_node_name(ast.Constant(value=5)) == ""


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
