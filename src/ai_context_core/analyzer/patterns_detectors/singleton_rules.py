"""Rules for identifying singleton pattern evidence."""

import ast
from ai_context_core.analyzer.constants import PATTERN_DETECTION_CONFIDENCE_HIGH

# --- Assign Rules ---


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


# --- Method Rules ---


def check_singleton_method(item: ast.FunctionDef, add_evidence_func) -> None:
    """Checks if a method is a singleton instance accessor."""
    if not _is_static_or_class_method(item):
        return

    if any(k in item.name.lower() for k in ("instance", "singleton", "get_inst")):
        add_evidence_func(
            f"Static/Class method '{item.name}' detected",
            PATTERN_DETECTION_CONFIDENCE_HIGH - 30,
        )


def _is_static_or_class_method(item: ast.FunctionDef) -> bool:
    """Helper to check if a function has a static or class method decorator."""
    for d in item.decorator_list:
        if isinstance(d, (ast.Name, ast.Attribute)):
            if getattr(d, "id", "") in ("classmethod", "staticmethod"):
                return True
            if getattr(d, "attr", "") in ("classmethod", "staticmethod"):
                return True
    return False


# --- General Rules ---


def check_singleton_item(item: ast.AST, add_evidence_func) -> None:
    """Checks a class body item for singleton evidence."""
    if isinstance(item, ast.FunctionDef) and item.name == "__new__":
        add_evidence_func("Overrides __new__ to control instantiation", 60)

    if isinstance(item, ast.FunctionDef):
        check_singleton_method(item, add_evidence_func)

    if isinstance(item, (ast.Assign, ast.AnnAssign)):
        check_singleton_assign(item, add_evidence_func)
