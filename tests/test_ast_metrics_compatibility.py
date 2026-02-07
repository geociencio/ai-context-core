import ast
from ai_context_core.analyzer.ast_metrics import calculate_sloc


def test_sloc_with_docstrings():
    """Test that SLOC calculation works correctly with docstrings on Python 3.14+."""
    code = """
\"\"\"Module docstring.\"\"\"

def foo():
    \"\"\"Function docstring.\"\"\"
    pass

class Bar:
    \"\"\"Class docstring.\"\"\"
    def baz(self):
        \"\"\"Method docstring.\"\"\"
        return 1
"""
    # Expected SLOC:
    # def foo(): -> 1 line
    #     pass -> 1 line
    # class Bar: -> 1 line
    #     def baz(self): -> 1 line
    #         return 1 -> 1 line
    # Total: 5 lines of code.
    # Docstrings and blank lines should be ignored.

    tree = ast.parse(code)
    sloc = calculate_sloc(tree, code)
    assert sloc == 5


def test_sloc_no_docstrings():
    code = """
def foo():
    pass
"""
    tree = ast.parse(code)
    sloc = calculate_sloc(tree, code)
    assert sloc == 2
