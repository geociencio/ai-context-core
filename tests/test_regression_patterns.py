from ai_context_core.analyzer.builders.qgis_scope import _match_path
from ai_context_core.analyzer.builders.git_patterns import GitPatternsSummarizer
from ai_context_core.analyzer.builders.patterns import PatternsBuilder


def test_git_patterns_summarizer_handles_missing_class():
    analyses = {"patterns": {"Observer": [{"confidence": 80, "evidence": ["e"]}]}}
    text = GitPatternsSummarizer(analyses).build_patterns()
    assert "N/A" in text
    assert "80" in text


def test_patterns_builder_handles_missing_class():
    lines = []
    analyses = {"patterns": {"Singleton": [{"confidence": 70}]}}
    PatternsBuilder(analyses).build(lines)
    assert "N/A" in "\n".join(lines)


def test_show_patterns_handles_missing_keys(capsys):
    from ai_context_core.cli.commands.report import _show_patterns

    _show_patterns({"patterns": {"Factory": [{"confidence": 60}]}})
    out = capsys.readouterr().out
    assert "N/A" in out
    assert "60" in out


def test_match_path_recursive_nested():
    assert _match_path("/project/gui/dialog.py", "gui/**/*.py") is True
    assert _match_path("/project/gui/sub/dialog.py", "gui/**/*.py") is True
    assert _match_path("/project/core/logic.py", "gui/**/*.py") is False


def test_match_path_windows_separators():
    assert _match_path(r"C:\project\gui\dialog.py", "gui/**/*.py") is True
    assert _match_path(r"C:\project\core\logic.py", "gui/**/*.py") is False
