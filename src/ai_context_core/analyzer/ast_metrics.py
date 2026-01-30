"""Code metrics calculation using AST analysis."""

import ast
from collections import Counter
from typing import Dict, Any


class TypeHintVisitor(ast.NodeVisitor):
    """Visitor to calculate type hint coverage."""

    def __init__(self):
        self.total_functions = 0
        self.typed_functions = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.total_functions += 1

        has_return_type = node.returns is not None
        args = [arg for arg in node.args.args if arg.arg not in ("self", "cls")]
        total_args = len(args)
        typed_args = sum(1 for arg in args if arg.annotation is not None)

        if has_return_type and (total_args == 0 or total_args == typed_args):
            self.typed_functions += 1

        self.generic_visit(node)


class HalsteadVisitor(ast.NodeVisitor):
    """Visitor to calculate Halstead metrics."""

    OPERATORS = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitXor,
        ast.BitAnd,
        ast.FloorDiv,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Invert,
        ast.UAdd,
        ast.USub,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.Is,
        ast.IsNot,
        ast.In,
        ast.NotIn,
        ast.If,
        ast.For,
        ast.While,
        ast.Try,
        ast.With,
        ast.FunctionDef,
        ast.ClassDef,
    )

    def __init__(self):
        self.operators = Counter()
        self.operands = Counter()

    def visit(self, node: ast.AST):
        """Override visit to check for operators and operands generically."""
        if isinstance(node, self.OPERATORS):
            self.operators[type(node).__name__] += 1
        elif isinstance(node, ast.Name):
            self.operands[node.id] += 1
        elif isinstance(node, ast.Constant):
            self.operands[str(node.value)] += 1
        super().visit(node)


def calculate_complexity(tree: ast.AST) -> int:
    """Calculates cyclomatic complexity of an AST tree."""
    # Note: Using import from complexity_visitor if available, otherwise implementing simple
    # logic here or assuming it was imported.
    # For now, let's implement a simple direct visitor or re-use existing logic.
    # The original file imported from .complexity_visitor inside the function.
    # We should probably port that logic here or maintain the import.
    # Assuming we want to consolidate code metrics.
    try:
        from .complexity_visitor import calculate_complexity as _calc_complexity

        return _calc_complexity(tree)
    except ImportError:
        # Fallback implementation if module missing
        return _simple_complexity(tree)


def _simple_complexity(tree: ast.AST) -> int:
    complexity = 1
    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.If,
                ast.While,
                ast.For,
                ast.Assert,
                ast.ExceptHandler,
                ast.With,
                ast.Try,
            ),
        ):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity


def calculate_type_hint_coverage(tree: ast.AST) -> Dict[str, Any]:
    """Calculates the percentage of functions with type hints."""
    visitor = TypeHintVisitor()
    visitor.visit(tree)

    total = visitor.total_functions
    typed = visitor.typed_functions
    coverage = (typed / total * 100) if total > 0 else 100.0

    return {
        "total_functions": total,
        "typed_functions": typed,
        "coverage": coverage,
    }


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
