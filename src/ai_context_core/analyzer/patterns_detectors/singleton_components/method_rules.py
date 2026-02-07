"""Rules for identifying singleton access methods."""

import ast
from ...constants import PATTERN_DETECTION_CONFIDENCE_HIGH


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
