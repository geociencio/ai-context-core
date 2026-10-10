"""Formatting logic for project-level complexity aggregation."""

from typing import List, Dict, Any

from . import metric_keys

# Complexity aggregation keys. Keys that are part of the canonical metric
# contract reuse the single source of truth in ``metric_keys``.
TOTAL_MODULES = "total_modules"
TOTAL_LINES = "total_lines"
TOTAL_PHYSICAL_LINES = metric_keys.TOTAL_PHYSICAL_LINES
TOTAL_FUNCTIONS = metric_keys.TOTAL_FUNCTIONS
TOTAL_CLASSES = metric_keys.TOTAL_CLASSES
AVERAGE_COMPLEXITY = metric_keys.AVERAGE_COMPLEXITY
AVG_MAINTENANCE_INDEX = metric_keys.AVG_MAINTENANCE_INDEX
MOST_COMPLEX_MODULES = "most_complex_modules"


def format_complexity_agg(
    valid_modules: List[Dict[str, Any]], project_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """Builds the complexity aggregation dictionary for backward compatibility."""
    return {
        TOTAL_MODULES: len(valid_modules),
        TOTAL_LINES: project_metrics.get(metric_keys.TOTAL_LINES_CODE, 0),
        TOTAL_PHYSICAL_LINES: project_metrics.get(metric_keys.TOTAL_PHYSICAL_LINES, 0),
        TOTAL_FUNCTIONS: project_metrics.get(metric_keys.TOTAL_FUNCTIONS, 0),
        TOTAL_CLASSES: project_metrics.get(metric_keys.TOTAL_CLASSES, 0),
        AVERAGE_COMPLEXITY: project_metrics.get(metric_keys.AVERAGE_COMPLEXITY, 0),
        AVG_MAINTENANCE_INDEX: project_metrics.get(metric_keys.AVG_MAINTENANCE_INDEX, 0),
        MOST_COMPLEX_MODULES: sorted(
            [(m["path"], m.get("complexity", 0)) for m in valid_modules],
            key=lambda x: x[1],
            reverse=True,
        )[:10],
    }
