import ast
from unittest.mock import patch
from ai_context_core.analyzer.visitors.sloc import calculate_sloc


def test_sloc_calculate_exception():
    # Coverage for sloc.py exception handling
    with patch(
        "ai_context_core.analyzer.visitors.sloc.tokenize.generate_tokens",
        side_effect=Exception("Tokenize fail"),
    ):
        # Should fallback to _calculate_sloc_fallback
        res = calculate_sloc(ast.parse("x=1"), "x=1")
        assert res == 1
