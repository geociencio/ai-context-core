"""Internal logic for singleton pattern detection."""

import ast
from .method_rules import check_singleton_method
from .assign_rules import check_singleton_assign


def check_singleton_item(item: ast.AST, add_evidence_func) -> None:
    """Checks a class body item for singleton evidence."""
    if isinstance(item, ast.FunctionDef) and item.name == "__new__":
        add_evidence_func("Overrides __new__ to control instantiation", 60)

    if isinstance(item, ast.FunctionDef):
        check_singleton_method(item, add_evidence_func)

    if isinstance(item, (ast.Assign, ast.AnnAssign)):
        check_singleton_assign(item, add_evidence_func)
