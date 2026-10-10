"""AST utilities for Python code analysis.

This module is a convenience facade re-exporting the specific submodules:
- ai_context_core.analyzer.visitors.ast_visitors
- ai_context_core.analyzer.visitors.ast_metrics
- ai_context_core.analyzer.visitors.ast_entry_points
"""

# Re-exports for backward compatibility
from .ast_visitors import (  # noqa: F401
    extract_functions,
    extract_classes,
    check_docstrings,
    extract_imports,
    detect_unused_imports,
)
from .ast_metrics import (  # noqa: F401
    calculate_complexity,
    calculate_halstead_metrics,
    calculate_type_hint_coverage,
    calculate_sloc,
)
from .ast_entry_points import (  # noqa: F401
    is_entry_point,
    has_main_guard,
)

__all__ = [
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
]
