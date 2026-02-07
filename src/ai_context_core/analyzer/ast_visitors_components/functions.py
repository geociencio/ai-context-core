"""Function extraction visitor."""

import ast
from typing import List

class FunctionVisitor(ast.NodeVisitor):
    """Visitor to extract function names and argument counts."""

    def __init__(self):
        """Initialize the FunctionVisitor."""
        self.functions = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits a function definition and extracts metadata."""
        func_info = node.name
        args_count = len(node.args.args)
        if args_count > 0:
            func_info = f"{func_info}({args_count} args)"
        self.functions.append(func_info)
        self.generic_visit(node)

def extract_functions(tree: ast.AST) -> List[str]:
    """Extracts function names and basic argument counts from an AST."""
    visitor = FunctionVisitor()
    visitor.visit(tree)
    return visitor.functions
