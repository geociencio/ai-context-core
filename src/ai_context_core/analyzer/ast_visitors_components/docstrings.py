"""Docstring presence checking visitor."""

import ast
from typing import Dict, Any


class DocstringVisitor(ast.NodeVisitor):
    """Visitor to check for docstring presence."""

    def __init__(self):
        """Initialize the DocstringVisitor."""
        self.docstrings = {"module": False, "classes": {}, "functions": {}}

    def visit_Module(self, node: ast.Module):
        """Visits the module node."""
        self.docstrings["module"] = ast.get_docstring(node) is not None
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits a class definition."""
        self.docstrings["classes"][node.name] = ast.get_docstring(node) is not None
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits a function definition."""
        self.docstrings["functions"][node.name] = ast.get_docstring(node) is not None
        self.generic_visit(node)


def check_docstrings(tree: ast.AST) -> Dict[str, Any]:
    """Checks for the presence of docstrings in modules, classes, and functions."""
    visitor = DocstringVisitor()
    visitor.visit(tree)
    return visitor.docstrings
