"""AST visitors and structural/metrics calculators (context-only)."""

from .ast_utils import (
    extract_base_name,
)
from .ast_visitors import (
    extract_functions,
    extract_classes,
    check_docstrings,
    extract_imports,
    detect_unused_imports,
)
from .ast_metrics import (
    calculate_complexity,
    calculate_halstead_metrics,
    calculate_type_hint_coverage,
    calculate_sloc,
)
from .ast_entry_points import (
    is_entry_point,
    has_main_guard,
)
from .complexity_visitor import ComplexityVisitor
from .visitors_base import BaseVisitor

__all__ = [
    "extract_base_name",
    "extract_functions",
    "extract_classes",
    "check_docstrings",
    "extract_imports",
    "detect_unused_imports",
    "calculate_complexity",
    "calculate_halstead_metrics",
    "calculate_type_hint_coverage",
    "calculate_sloc",
    "is_entry_point",
    "has_main_guard",
    "ComplexityVisitor",
    "BaseVisitor",
]
