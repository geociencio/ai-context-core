"""Complexity analysis utilities for ai-context-core."""

import ast
from typing import Set


class ComplexityVisitor(ast.NodeVisitor):
    """Visitor to calculate cyclomatic complexity."""

    def __init__(self):
        self.complexity = 0
        self.decision_lines = set()

    def _add_decision(self, node):
        self.complexity += 1
        if hasattr(node, "lineno"):
            self.decision_lines.add(node.lineno)

    def visit_If(self, node: ast.If):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self._add_decision(node)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        self.complexity += len(node.generators)
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp):
        self.complexity += len(node.generators)
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp):
        self.complexity += len(node.generators)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        self.complexity += len(node.generators)
        self.generic_visit(node)


def calculate_complexity(tree: ast.AST) -> int:
    """Calculates optimized cyclomatic complexity.

    Args:
        tree: The AST tree to analyze

    Returns:
        The calculated complexity score
    """
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    return _apply_complexity_penalty(visitor.complexity, visitor.decision_lines)


def _apply_complexity_penalty(complexity: int, decision_lines: Set[int]) -> int:
    """Applies a penalty for highly dense logic (many decisions in few lines).

    Args:
        complexity: The base complexity score
        decision_lines: Set of line numbers with decision points

    Returns:
        The adjusted complexity score with penalty applied
    """
    from .constants import (
        COMPLEXITY_PENALTY_DENSITY_THRESHOLD,
        COMPLEXITY_PENALTY_MULTIPLIER,
    )

    if not decision_lines:
        return complexity

    line_range = max(decision_lines) - min(decision_lines) + 1
    density = len(decision_lines) / line_range

    if density > COMPLEXITY_PENALTY_DENSITY_THRESHOLD:
        return int(complexity * COMPLEXITY_PENALTY_MULTIPLIER)

    return complexity
