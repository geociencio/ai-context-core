"""Halstead metrics calculation logic."""

import ast
from collections import Counter
from typing import Dict, Any

class HalsteadVisitor(ast.NodeVisitor):
    """Visitor to calculate Halstead metrics indicators."""

    OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv, ast.And, ast.Or, ast.Not,
        ast.Invert, ast.UAdd, ast.USub, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt,
        ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.If, ast.For, ast.While,
        ast.Try, ast.With, ast.FunctionDef, ast.ClassDef,
    )

    def __init__(self):
        """Initialize counters."""
        self.operators = Counter()
        self.operands = Counter()

    def visit(self, node: ast.AST):
        """Record operators and operands."""
        if isinstance(node, self.OPERATORS):
            self.operators[type(node).__name__] += 1
        elif isinstance(node, ast.Name):
            self.operands[node.id] += 1
        elif isinstance(node, ast.Constant):
            self.operands[str(node.value)] += 1
        super().visit(node)

def calculate_halstead_metrics(tree: ast.AST) -> Dict[str, Any]:
    """Calculates basic Halstead complexity metrics."""
    visitor = HalsteadVisitor()
    visitor.visit(tree)

    n1 = len(visitor.operators)
    n2 = len(visitor.operands)
    N1 = sum(visitor.operators.values())
    N2 = sum(visitor.operands.values())

    h_vocabulary = n1 + n2
    h_length = N1 + N2

    if n1 > 0 and n2 > 0:
        h_volume = h_length * (h_vocabulary.bit_length() - 1)
        h_difficulty = (n1 / 2) * (N2 / n2)
        h_effort = h_difficulty * h_volume
    else:
        h_volume = h_difficulty = h_effort = 0

    return {
        "vocabulary": h_vocabulary,
        "length": h_length,
        "volume": round(h_volume, 2),
        "difficulty": round(h_difficulty, 2),
        "effort": round(h_effort, 2),
    }
