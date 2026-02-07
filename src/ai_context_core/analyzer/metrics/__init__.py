"""Metrics calculation and quality scoring for ai-context-core."""

from typing import Dict, Any, List
from .calculator import (
    MetricsCalculator,
    calculate_maintenance_index,
    calculate_halstead_metrics,
)
from .scorer import ProjectScorer

__all__ = [
    "MetricsCalculator",
    "ProjectScorer",
    "calculate_maintenance_index",
    "calculate_halstead_metrics",
]


def calculate_project_metrics(
    modules_data: List[Dict[str, Any]],
    entry_points: List[str],
    test_files_count: int,
    config: Dict[str, Any],
    ctx: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculates overall project metrics and quality score.

    Args:
        modules_data: List of module analysis results.
        entry_points: List of entry point paths.
        test_files_count: Number of test files.
        config: Analyzer configuration.
        ctx: Global analysis context.

    Returns:
        Dictionary containing project-level metrics.
    """
    total_physical = sum(m.get("lines", 0) for m in modules_data)
    total_sloc = sum(m.get("sloc", 0) for m in modules_data)

    # functions and classes are lists in modules_data
    total_functions = sum(
        (
            len(m.get("functions", []))
            if isinstance(m.get("functions"), list)
            else m.get("functions", 0)
        )
        for m in modules_data
    )
    total_classes = sum(
        (
            len(m.get("classes", []))
            if isinstance(m.get("classes"), list)
            else m.get("classes", 0)
        )
        for m in modules_data
    )

    complexity_list = [m.get("complexity", 0) for m in modules_data]
    avg_complexity = (
        sum(complexity_list) / len(complexity_list) if complexity_list else 0
    )

    total_docstrings = sum(
        1 for m in modules_data if m.get("docstrings", {}).get("module")
    )
    doc_coverage = (total_docstrings / len(modules_data) * 100) if modules_data else 0

    scorer = ProjectScorer(config)
    quality_score = scorer.calculate(modules_data, ctx)

    mi_list = [
        m.get("maintenance_index", 0) for m in modules_data if "maintenance_index" in m
    ]
    avg_mi = sum(mi_list) / len(mi_list) if mi_list else 0

    return {
        "total_physical_lines": total_physical,
        "total_lines_code": total_sloc,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "average_complexity": round(avg_complexity, 2),
        "quality_score": quality_score,
        "docstring_coverage": round(doc_coverage, 2),
        "avg_maintenance_index": round(avg_mi, 2),
        "test_files_count": test_files_count,
    }
