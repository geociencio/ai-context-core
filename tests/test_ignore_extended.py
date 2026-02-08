import pathlib
from ai_context_core.analyzer.providers.ignore_filter import load_ignore_patterns
from ai_context_core.analyzer.ignore_filter import IgnoreFilter


def test_load_ignore_patterns_file_exists(tmp_path):
    p = tmp_path / ".analyzerignore"
    p.write_text("*.log\ntemp/\n# comment\n")
    patterns = load_ignore_patterns(tmp_path)
    assert "*.log" in patterns
    assert "temp/" in patterns
    assert "# comment" not in patterns


def test_load_ignore_patterns_exception(tmp_path):
    p = tmp_path / ".analyzerignore"
    p.mkdir()  # Cause error on open()
    # Should fallback to defaults
    patterns = load_ignore_patterns(tmp_path)
    assert ".git" in patterns


def test_load_ignore_patterns_extra(tmp_path):
    patterns = load_ignore_patterns(tmp_path, extra_patterns=["*.tmp"])
    assert "*.tmp" in patterns


def test_ignore_filter_logic(tmp_path):
    # Fixed test to use extra_patterns and is_ignored
    filt = IgnoreFilter(tmp_path, extra_patterns=["*.log", "secret/"])

    # Matching file
    assert filt.is_ignored(tmp_path / "app.log") is True

    # Matching dir
    assert filt.is_ignored(tmp_path / "secret" / "keys.txt") is True

    # Non-matching
    assert filt.is_ignored(tmp_path / "main.py") is False

    # Relative path matching
    assert filt.is_ignored(pathlib.Path("secret/data.json")) is True
