"""Handles verification of i18n calls (tr, translate)."""

import ast
from typing import Dict, Any

def handle_i18n_call(node: ast.Call, results: Dict[str, Any]) -> None:
    """Checks for tr() or translate() calls and updates results."""
    if not isinstance(node.func, ast.Attribute):
        return
        
    if node.func.attr == "tr":
        results["i18n_usage"]["tr"] += 1
    elif node.func.attr == "translate":
        results["i18n_usage"]["translate"] += 1
