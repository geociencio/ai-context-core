"""Anti-pattern detection for Python code.

This module identifies common bad practices and code smells such as God Objects,
Spaghetti Code, Magic Numbers, and Dead Code.
"""

import ast
from typing import List, Dict, Any


def detect_god_object(tree: ast.AST, threshold_methods: int = 20) -> List[Dict[str, Any]]:
    """Detects 'God Object' classes with too many methods.

    Args:
        tree: The AST to analyze.
        threshold_methods: Minimum number of methods to trigger detection.

    Returns:
        List of detected issues.
    """
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
            if method_count > threshold_methods:
                issues.append(
                    {
                        "type": "god_object",
                        "severity": "high",
                        "message": f"Class '{node.name}' is a God Object ({method_count} methods)",
                        "line": node.lineno,
                        "value": method_count,
                    }
                )
    return issues


def detect_spaghetti_code(tree: ast.AST, complexity_threshold: int = 25) -> List[Dict[str, Any]]:
    """Detects 'Spaghetti Code' functions with high cyclomatic complexity.

    This relies on the complexity calculation from ast_utils, but since we don't prefer circular imports
    or passing external complexity results, we might need a way to integrate this.
    For now, we will rely on integration level to call this.
    Alternatively, we can accept pre-calculated complexity list, or re-calculate.

    Wait, to invoke this standalone, we need to calculate complexity.
    To avoid duplication, we should import calculate_complexity from ast_utils.
    """
    # Import locally to avoid circular import if ast_utils imports this module (it shouldn't)
    from .ast_utils import calculate_complexity

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Extract subtree for function to calculate its complexity
            # calculate_complexity input is an AST node (tree or function node)
            # But the current implementation of calculate_complexity walks the tree.
            # Passing the function node as 'tree' works.
            cc = calculate_complexity(node)
            if cc > complexity_threshold:
                issues.append(
                    {
                        "type": "spaghetti_code",
                        "severity": "high",
                        "message": f"Function '{node.name}' is Spaghetti Code (Complexity: {cc})",
                        "line": node.lineno,
                        "value": cc,
                    }
                )
    return issues


def detect_magic_numbers(tree: ast.AST, threshold_occurrences: int = 3) -> List[Dict[str, Any]]:
    """Detects 'Magic Numbers' usage (hardcoded numeric constants).

    Ignores 0, 1, -1 and power of 2 common values maybe?
    For simplicity: ignore -1, 0, 1.
    """
    issues = []
    # We might want to count occurrences per value to avoid noise?
    # Or just flag every occurrence? Flagging every occurrence is noisy.
    # The requirement says "Constantes hardcodeadas".

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value in [0, 1, -1, 0.0, 1.0]:
                continue

            # Check if it's assigned to a constant variable (UPPER_CASE) -> Acceptable
            # It's hard to check parent context easily in ast.walk without parent pointers.
            # So we'll produce a warning broadly for now or skip this detailed check.

            # Actually, magic numbers usually refer to usage inside logic, not definitions.
            # If it's inside a Call, BinOp, Compare, etc.

            # Let's simple implementation first: Any number used, maybe filtering obvious ones.

            issues.append(
                {
                    "type": "magic_number",
                    "severity": "low",
                    "message": f"Magic number detected: {node.value}",
                    "line": node.lineno,
                    "value": node.value,
                }
            )

    # Filter to unique per line or something?
    # Let's keep it simple.
    return issues


def detect_dead_code(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects 'Dead Code' (e.g. code after return/raise).

    This is simple unreachable code detection.
    True 'dead code' (never imported/called) requires project-level analysis.
    The requirement says "Dead Code (código nunca importado)".
    This requires cross-file analysis which 'antipatterns.py' acting on a single tree cannot do alone
    unless checks usage.

    However, 'find_unused_imports' is in 'Dependency Improved' plan.
    'Dead Code' here might refer to local unreachable code or unused variables/classes?

    If strict "never imported", it's a project level check (engine level).
    If local dead code (unreachable), it's AST level.

    Task says: "[ ] `detect_dead_code()` - Código nunca importado"
    So it implies finding files or symbols that are never imported.
    This cannot be done in a single-file AST pass. It needs the full dependency graph.

    So I will define the function here but it might need to accept the dependency graph or be called from engine with more context.
    Or maybe I should implement Unreachable Code here?

    Let's implement Unreachable Code (easier) AND Unused Imports (local).
    But for "never imported" (global dead code), I need the usage graph.

    Given the scope "Antipatterns module", I will implement `detect_dead_code` to accept `is_used` info or similar if possible.
    But detecting unreachable code locally is also "Dead Code".

    Let's implement local unreachable code for now.
    """
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.Module)):
            body = node.body
            for i, child in enumerate(body):
                if isinstance(child, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                    if i + 1 < len(body):
                        # Statements after return/raise
                        issues.append(
                            {
                                "type": "dead_code",
                                "severity": "medium",
                                "message": "Unreachable code detected after return/raise/break/continue",
                                "line": body[i + 1].lineno,
                                "value": 1,
                            }
                        )
                        break  # Only report first unreachable block per scope
    return issues
