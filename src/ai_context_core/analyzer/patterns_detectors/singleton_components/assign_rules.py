"""Rules for identifying singleton instance variables."""

import ast


def check_singleton_assign(item: ast.AST, add_evidence_func) -> None:
    """Checks for static instance variables."""
    targets = item.targets if isinstance(item, ast.Assign) else [item.target]
    for t in targets:
        if _is_singleton_instance_var(t):
            add_evidence_func(f"Static instance variable '{t.id}' found", 20)


def _is_singleton_instance_var(target: ast.AST) -> bool:
    """Helper to check if a variable name indicates a singleton instance."""
    if not isinstance(target, ast.Name):
        return False
    return any(k in target.id.lower() for k in ("instance", "_inst"))
