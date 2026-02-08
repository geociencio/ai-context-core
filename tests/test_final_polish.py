import ast
from ai_context_core.analyzer.html_builder import HTMLBuilder
from ai_context_core.analyzer.visitors.sloc import calculate_sloc
from unittest.mock import patch


def test_html_builder_empty_list():
    # Test html_builder.py line 62
    builder = HTMLBuilder("Test")
    assert builder.build_list([]) == ""


def test_sloc_fallback_on_error():
    # Test sloc.py line 36
    with patch("tokenize.generate_tokens") as mock_gen:
        mock_gen.side_effect = Exception("Tokenize error")
        content = "def foo():\n    pass # comment\n\n# another"
        # _fallback_sloc skips comments and blanks
        # Lines: 'def foo():' (1), 'pass' (1) -> 2
        # Pass a valid empty AST to avoid walking None
        tree = ast.parse("")
        assert calculate_sloc(tree, content) == 2


def test_sloc_extra_ignored_tokens():
    # Coverage for _should_skip_token variants if needed
    # (tokenize.NL is used for blanks in multi-line)
    content = "x = 1\n\n    \ny = 2"
    # x=1 (valid), blank (NL), space-only-blank (NL), y=2 (valid)
    # SLOC should be 2
    assert calculate_sloc(ast.parse(content), content) == 2
