"""Project quality metrics and scoring algorithms.

Defines the logic for calculating cyclomatic distribution, overall
quality scores based on weights, and aggregated project metrics.
"""

import math
from typing import List, Dict, Any


def calculate_complexity_distribution(
    modules_data: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Calculates the distribution of cyclomatic complexity across modules.

    Args:
        modules_data: List of module metrics dictionaries.

    Returns:
        A dictionary with complexity buckets (low, medium, high, very_high) and counts.
    """
    distribution = {
        "low (0-5)": 0,
        "medium (6-15)": 0,
        "high (16-30)": 0,
        "very_high (31+)": 0,
    }

    for module in modules_data:
        complexity = module.get("complexity", 0)
        if complexity <= 5:
            distribution["low (0-5)"] += 1
        elif complexity <= 15:
            distribution["medium (6-15)"] += 1
        elif complexity <= 30:
            distribution["high (16-30)"] += 1
        else:
            distribution["very_high (31+)"] += 1

    return distribution


def calculate_maintenance_index(
    halstead_volume: float, cyclomatic_complexity: int, lines_of_code: int
) -> float:
    """Calculates the Maintenance Index (MI) for a module.

    Uses the SEI formula:
    MI = 171 - 5.2 * ln(V) - 0.23 * (G) - 16.2 * ln(LOC)

    Args:
        halstead_volume: Halstead Volume (V).
        cyclomatic_complexity: Cyclomatic Complexity (G).
        lines_of_code: Lines of Code (LOC).

    Returns:
        The Maintenance Index, typically between 0 and 100 (though formula can go higher).
    """
    if halstead_volume <= 0 or lines_of_code <= 0:
        return 100.0

    # SEI formula
    mi = (
        171
        - 5.2 * math.log(halstead_volume)
        - 0.23 * cyclomatic_complexity
        - 16.2 * math.log(lines_of_code)
    )

    # Normalize to 0-100 scale (Microsoft variation uses different normalization but SEI is the base)
    normalized_mi = (mi * 100) / 171

    return round(max(0, min(100, normalized_mi)), 2)


def calculate_quality_score(
    modules_data: List[Dict[str, Any]],
    config: Dict[str, Any],
    context_patterns: Dict[str, Any],
) -> float:
    """Calculates an overall quality score for the project based on weighted metrics.

    Evaluates documentation, complexity, file size, and syntax correctness. It
    also factors in QGIS compliance if applicable and penalizes for linter errors.

    Args:
        modules_data: List of analyzed module dictionaries.
        config: Configuration containing quality weights and thresholds.
        context_patterns: Additional context data like QGIS compliance and linter info.

    Returns:
        A normalized quality score between 0 and 100.
    """
    if not modules_data:
        return 0.0

    weights = config.get("quality_weights", {})
    thresholds = config.get("thresholds", {})

    # Calculate maximum possible score per module
    max_module_score = (
        weights.get("docstrings", 0)
        + weights.get("complexity_low", 0)
        + weights.get("size_small", 0)
        + weights.get("has_main", 0)
        + weights.get("no_syntax_error", 0)
    )

    total_score = 0.0
    max_possible_total = len(modules_data) * max_module_score

    for module in modules_data:
        module_score = 0

        # Points for having docstrings
        if module.get("docstrings", {}).get("module", False):
            module_score += weights.get("docstrings", 0)

        # Points for low complexity
        complexity = module.get("complexity", 0)
        if complexity <= thresholds.get("complexity_low", 5):
            module_score += weights.get("complexity_low", 0)
        elif complexity <= thresholds.get("complexity_medium", 10):
            module_score += weights.get("complexity_medium", 0)
        elif complexity <= thresholds.get("complexity_high", 15):
            module_score += weights.get("complexity_high", 0)

        # Points for adequate file size
        lines = module.get("lines", 0)
        if lines <= thresholds.get("size_small", 200):
            module_score += weights.get("size_small", 0)
        elif lines <= thresholds.get("size_medium", 400):
            module_score += weights.get("size_medium", 0)

        # Points for having a main guard
        if module.get("has_main", False):
            module_score += weights.get("has_main", 0)

        # Points for no syntax errors
        if not module.get("syntax_error", False):
            module_score += weights.get("no_syntax_error", 0)

        total_score += module_score

    # Normalize to percentage
    final_score = (total_score / max_possible_total) * 100 if max_possible_total > 0 else 0

    # Factor in QGIS compliance score if present
    qgis_data = context_patterns.get("qgis_compliance", {})
    qgis_score = qgis_data.get("compliance_score")

    if qgis_score is not None:
        # Final score is weighted: 70% Code Quality, 30% QGIS Standards
        final_score = (final_score * 0.7) + (qgis_score * 0.3)

    # Penalty for linter errors
    linter_data = context_patterns.get("linter", {})
    if linter_data.get("available"):
        errors = linter_data.get("errors", 0)
        # Penalize 0.5 points per error, max 10 points
        penalty = min(10, errors * 0.5)
        final_score = max(0, final_score - penalty)

    return round(final_score, 1)


def calculate_project_metrics(
    modules_data: List[Dict[str, Any]],
    context_entry_points: List[str],
    test_files_count: int,
    config: Dict[str, Any],
    context_patterns: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculates general project-level metrics from analyzed modules.

    Args:
        modules_data: List of module analysis objects.
        context_entry_points: List of identified entry point paths.
        test_files_count: Total count of test files in the project.
        config: Metric weights and thresholds configuration.
        context_patterns: Additional scoring data (QGIS, Linter).

    Returns:
        A dictionary containing aggregated metrics like totals, averages, and quality score.
    """
    if not modules_data:
        return {}

    total_size_kb = sum(m.get("file_size_kb", 0) for m in modules_data)
    total_lines = sum(m.get("lines", 0) for m in modules_data)

    # Calculate documentation coverage
    total_doc_score = 0
    total_symbols = 0

    for m in modules_data:
        m_docs = m.get("docstrings", {})
        # Module docstring (binary)
        total_symbols += 1
        if m_docs.get("module", False):
            total_doc_score += 1

        # Classes
        classes = m_docs.get("classes", {})
        total_symbols += len(classes)
        total_doc_score += sum(1 for documented in classes.values() if documented)

        # Functions
        functions = m_docs.get("functions", {})
        total_symbols += len(functions)
        total_doc_score += sum(1 for documented in functions.values() if documented)

    doc_coverage = (total_doc_score / total_symbols * 100) if total_symbols > 0 else 0

    modules_with_main = sum(1 for m in modules_data if m.get("has_main", False))
    modules_with_syntax_error = sum(1 for m in modules_data if m.get("syntax_error", False))

    # Complexity statistics
    complexities = [m.get("complexity", 0) for m in modules_data]
    avg_complexity = sum(complexities) / len(complexities) if complexities else 0

    # Coverage metrics
    type_hint_cov = [m.get("type_hints", {}).get("coverage", 100) for m in modules_data]
    i18n_scores = [m.get("i18n", {}).get("i18n_score", 100) for m in modules_data]

    # Maintenance Index
    mi_scores = [m.get("maintenance_index", 100) for m in modules_data if not m.get("syntax_error")]
    avg_mi = sum(mi_scores) / len(mi_scores) if mi_scores else 100

    return {
        "total_size_kb": round(total_size_kb, 2),
        "total_lines_code": total_lines,
        "avg_module_size_kb": round(total_size_kb / len(modules_data), 2),
        "avg_lines_per_module": round(total_lines / len(modules_data), 2),
        "modules_with_docstrings": sum(
            1 for m in modules_data if m.get("docstrings", {}).get("module", False)
        ),
        "modules_with_main_guard": modules_with_main,
        "modules_with_syntax_errors": modules_with_syntax_error,
        "docstring_coverage": round(doc_coverage, 2),
        "type_hint_coverage": (
            round(sum(type_hint_cov) / len(modules_data), 2) if modules_data else 0
        ),
        "i18n_coverage": (round(sum(i18n_scores) / len(modules_data), 2) if modules_data else 0),
        "entry_points_count": len(context_entry_points),
        "test_files_count": test_files_count,
        "avg_complexity": round(avg_complexity, 2),
        "max_complexity": max(complexities) if complexities else 0,
        "avg_maintenance_index": round(avg_mi, 2),
        "quality_score": calculate_quality_score(modules_data, config, context_patterns),
    }
