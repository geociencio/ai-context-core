"""Signal detection for PyQt and custom signals."""

import ast


def detect_signals(node: ast.AST) -> int:
    """Counts signal definitions in a node."""
    signals_found = 0
    for item in ast.iter_child_nodes(node):
        if _is_signal_definition(item):
            signals_found += 1
    return signals_found


def _is_signal_definition(node: ast.AST) -> bool:
    """Helper to determine if an AST node defines a signal."""
    if not isinstance(node, (ast.Assign, ast.AnnAssign)):
        return False

    val = node.value
    if not (val and isinstance(val, ast.Call)):
        return False

    try:
        func_str = ast.unparse(val.func).lower()
        return "pyqtsignal" in func_str or "signal" in func_str
    except Exception:
        return False
