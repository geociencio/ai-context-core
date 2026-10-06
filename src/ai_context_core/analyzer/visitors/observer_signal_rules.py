"""Signal detection rules for the observer pattern."""

import ast


def detect_signals(node: ast.AST) -> int:
    """Count signal definitions in a node."""
    signals_found = 0
    for item in ast.iter_child_nodes(node):
        if _is_signal_definition(item):
            signals_found += 1
    return signals_found


def _is_signal_definition(node: ast.AST) -> bool:
    """Determine if an AST node defines a signal."""
    if not isinstance(node, (ast.Assign, ast.AnnAssign)):
        return False

    val = node.value
    if not (val and isinstance(val, ast.Call)):
        return False

    return _signal_call_name(val.func) in {"pyqtsignal", "signal"}


def _signal_call_name(func: ast.AST) -> str:
    """Return the trailing name of a signal constructor call, lowercased."""
    if isinstance(func, ast.Name):
        return func.id.lower()
    if isinstance(func, ast.Attribute):
        return func.attr.lower()
    return ""
