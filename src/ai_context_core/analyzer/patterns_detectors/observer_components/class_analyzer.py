"""Internal class analysis logic for observer patterns."""

import ast
from .collections import (
    check_init_assign,
    check_mgmt_method,
    check_notify_method,
    check_iteration,
)


def analyze_class_body(node: ast.ClassDef, add_evidence_func) -> None:
    """Analyzes class body for observer patterns."""
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            _check_init(item, add_evidence_func)
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_method(item, add_evidence_func)


def _check_init(node: ast.FunctionDef, add_evidence_func) -> None:
    """Checks __init__ for observer collection initialization."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Assign) and check_init_assign(sub):
            add_evidence_func("Observer collection initialized in __init__", 20)

        if isinstance(sub, ast.Call):
            _check_connection_call(sub, add_evidence_func)


def _check_connection_call(node: ast.Call, add_evidence_func) -> None:
    """Checks if a call node is a signal connection."""
    try:
        func_name = ast.unparse(node.func).lower()
        if ".connect" in func_name:
            add_evidence_func(f"Signal connection detected: {func_name}", 10)
    except Exception:
        pass


def _check_method(node: ast.FunctionDef, add_evidence_func) -> None:
    """Checks a method for observer management or notification."""
    if check_mgmt_method(node.name):
        add_evidence_func(f"Management method '{node.name}' detected", 15)

    if check_notify_method(node.name):
        _analyze_notification_method(node, add_evidence_func)


def _analyze_notification_method(node: ast.FunctionDef, add_evidence_func) -> None:
    """Helper to analyze a potential notification method."""
    add_evidence_func(f"Notification method '{node.name}' detected", 15)
    if check_iteration(node):
        add_evidence_func("Notification method iterates over collection", 30)
