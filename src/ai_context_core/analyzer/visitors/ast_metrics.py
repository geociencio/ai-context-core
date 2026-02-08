"""Metrics calculation for Python AST (Complexity, Halstead, Type Hints)."""

import ast
from collections import Counter
from typing import Dict, Any


class TypeHintVisitor(ast.NodeVisitor):
    """Visitor to calculate type hint coverage."""

    def __init__(self):
        """Initialize the visitor."""
        self.total_functions = 0
        self.typed_functions = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits a function definition to check for type hints.

        Args:
            node: The FunctionDef node.
        """
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
        """Initialize the visitor counters."""
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
    """Calculates cyclomatic complexity of an AST tree.

    Delegates to ComplexityVisitor for detailed branching analysis.

    Args:
        tree: The AST to analyze.

    Returns:
        Cyclomatic complexity value.
    """
    from .complexity_visitor import calculate_complexity as _calc_complexity

    return _calc_complexity(tree)


def calculate_type_hint_coverage(tree: ast.AST) -> Dict[str, Any]:
    """Calculates the percentage of functions with type hints.

    Args:
        tree: The AST to analyze.

    Returns:
        Dictionary with total_functions, typed_functions, and coverage.
    """
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
    """Calculates basic Halstead complexity metrics.

    Args:
        tree: The AST to analyze.

    Returns:
        Dictionary of Halstead metrics.
    """
    from .halstead import calculate_halstead_metrics as _calc_halstead

    return _calc_halstead(tree)


def calculate_sloc(tree: ast.AST, content: str) -> int:
    """Calculates Source Lines of Code (SLOC).

    Excludes blank lines, comments, and docstrings.

    Args:
        tree: The AST of the module.
        content: The raw source code string.

    Returns:
        The count of real source lines of code.
    """
    from .sloc import calculate_sloc as _calc_sloc

    return _calc_sloc(tree, content)
