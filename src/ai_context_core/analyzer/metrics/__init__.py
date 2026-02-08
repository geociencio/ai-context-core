"""Compatibility facade for metrics."""

# Compatibility layer for tests
try:
    from ..builders.scorer import ProjectScorer
    from ..builders.calculator import (
        MetricsCalculator,
        calculate_maintenance_index,
        calculate_halstead_metrics,
        calculate_project_metrics,
    )
except ImportError:
    # If called from a context where relative imports fail
    from ai_context_core.analyzer.builders.scorer import ProjectScorer
    from ai_context_core.analyzer.builders.calculator import (
        MetricsCalculator,
        calculate_maintenance_index,
        calculate_halstead_metrics,
        calculate_project_metrics,
    )

__all__ = [
    "ProjectScorer",
    "MetricsCalculator",
    "calculate_maintenance_index",
    "calculate_halstead_metrics",
    "calculate_project_metrics",
]
