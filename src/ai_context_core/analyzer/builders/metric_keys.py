"""Shared metric key constants for a single producer/consumer contract."""

from typing import Dict, Any, FrozenSet, List

QUALITY_SCORE = "quality_score"
TOTAL_LINES_CODE = "total_lines_code"
TOTAL_PHYSICAL_LINES = "total_physical_lines"
TOTAL_FUNCTIONS = "total_functions"
TOTAL_CLASSES = "total_classes"
AVERAGE_COMPLEXITY = "average_complexity"
MAX_COMPLEXITY = "max_complexity"
AVG_MAINTENANCE_INDEX = "avg_maintenance_index"
TEST_FILES_COUNT = "test_files_count"
ENTRY_POINTS_COUNT = "entry_points_count"
SCORE_BREAKDOWN = "score_breakdown"

PROJECT_METRIC_KEYS: FrozenSet[str] = frozenset(
    {
        QUALITY_SCORE,
        TOTAL_LINES_CODE,
        TOTAL_PHYSICAL_LINES,
        TOTAL_FUNCTIONS,
        TOTAL_CLASSES,
        AVERAGE_COMPLEXITY,
        MAX_COMPLEXITY,
        AVG_MAINTENANCE_INDEX,
        TEST_FILES_COUNT,
        ENTRY_POINTS_COUNT,
        SCORE_BREAKDOWN,
    }
)


def missing_metric_keys(metrics: Dict[str, Any]) -> List[str]:
    """Return the expected metric keys absent from a metrics dict."""
    return [key for key in PROJECT_METRIC_KEYS if key not in metrics]
