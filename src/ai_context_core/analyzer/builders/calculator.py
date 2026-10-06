"""Core metrics calculation logic (MI, Halstead, etc.)."""

import math
from typing import Dict, Any, Optional

from . import metric_keys

# Default ai-ctx Quality Score knobs. Every value is additive and overridable
# through the ``[scoring]`` section of the project config.
DEFAULT_SCORING_CONFIG: Dict[str, float] = {
    "base_score": 100.0,
    "complexity_medium_threshold": 15.0,
    "complexity_medium_penalty_per_point": 2.0,
    "complexity_high_threshold": 25.0,
    "complexity_high_penalty_per_point": 0.5,
    "complexity_high_penalty_cap": 10.0,
    "maintainability_threshold": 65.0,
    "maintainability_penalty_per_point": 1.5,
    "no_tests_penalty": 20.0,
    "tests_bonus_per_file": 2.0,
    "tests_bonus_cap": 10.0,
}


def _resolve_scoring(config: Dict[str, Any]) -> Dict[str, float]:
    """Merge user scoring config over defaults, honoring legacy thresholds.

    Args:
        config: Full analyzer configuration dictionary.

    Returns:
        Resolved scoring configuration with every knob present.
    """
    resolved = dict(DEFAULT_SCORING_CONFIG)
    resolved.update(config.get("scoring", {}) or {})

    # Back-compat: legacy "thresholds" section overrides complexity thresholds.
    thresholds = config.get("thresholds", {}) or {}
    if "complexity_medium" in thresholds:
        resolved["complexity_medium_threshold"] = thresholds["complexity_medium"]
    if "complexity_high" in thresholds:
        resolved["complexity_high_threshold"] = thresholds["complexity_high"]
    return resolved


class MetricsCalculator:
    """Class to calculate basic code metrics."""

    @staticmethod
    def maintenance_index(v: float, g: int, loc: int) -> float:
        """Calculates the Maintenance Index (MI).

        Formula based on SEI standards, normalized to 0-100.

        Args:
            v: Halstead Volume.
            g: Cyclomatic Complexity.
            loc: Lines of Code (Source).

        Returns:
            Normalized Maintenance Index.
        """
        if v <= 0 or loc <= 0:
            return 100.0
        mi = 171 - 5.2 * math.log(v) - 0.23 * g - 16.2 * math.log(loc)
        return round(max(0, min(100, (mi * 100) / 171)), 2)

    @staticmethod
    def halstead_metrics(n1: int, n2: int, N1: int, N2: int) -> Dict[str, float]:
        """Calculates Halstead metrics.

        Args:
            n1: Number of unique operators.
            n2: Number of unique operands.
            N1: Total number of operators.
            N2: Total number of operands.

        Returns:
            Dictionary with volume, difficulty, and effort.
        """
        n = n1 + n2
        N = N1 + N2
        v = N * math.log2(n) if n > 0 else 0
        d = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        e = d * v
        return {"volume": v, "difficulty": d, "effort": e}


def calculate_maintenance_index(v: float, g: int, loc: int) -> float:
    """Standalone function to calculate Maintenance Index.

    Args:
        v: Halstead Volume.
        g: Cyclomatic Complexity.
        loc: Lines of Code (Source).

    Returns:
        Normalized Maintenance Index.
    """
    return MetricsCalculator.maintenance_index(v, g, loc)


def calculate_halstead_metrics(n1: int, n2: int, N1: int, N2: int) -> Dict[str, float]:
    """Standalone function to calculate Halstead metrics.

    Args:
        n1: Number of unique operators.
        n2: Number of unique operands.
        N1: Total number of operators.
        N2: Total number of operands.

    Returns:
        Dictionary with volume, difficulty, and effort.
    """
    return MetricsCalculator.halstead_metrics(n1, n2, N1, N2)


def calculate_project_metrics(
    modules: list[Dict[str, Any]],
    entry_points: list[str],
    test_files_count: Optional[int],
    config: Dict[str, Any],
    extra_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Calculate aggregated project metrics.

    Args:
        modules: List of module analysis results.
        entry_points: List of entry point/main file paths.
        test_files_count: Number of test files found, or None if unevaluated.
        config: Configuration dictionary.
        extra_data: Additional data like QGIS compliance results.

    Returns:
        Dictionary with aggregated project metrics.
    """
    total_loc = sum(m.get("sloc", m.get("loc", 0)) for m in modules)
    total_physical = sum(m.get("lines", 0) for m in modules)
    total_functions = sum(len(m.get("functions", [])) for m in modules)
    total_classes = sum(len(m.get("classes", [])) for m in modules)
    total_complexity = sum(m.get("complexity", 0) for m in modules)
    avg_complexity = total_complexity / len(modules) if modules else 0
    max_complexity = max((m.get("complexity", 0) for m in modules), default=0)

    # Calculate maintainability
    total_mi = sum(m.get("maintenance_index", 100) for m in modules)
    avg_mi = total_mi / len(modules) if modules else 100

    # Calculate Quality Score as an explicit, configurable breakdown.
    scoring = _resolve_scoring(config)
    breakdown: Dict[str, float] = {"base": float(scoring["base_score"])}

    # Deduct for average complexity.
    complexity_penalty = 0.0
    medium_cfg = scoring["complexity_medium_threshold"]
    if avg_complexity > medium_cfg:
        complexity_penalty = (avg_complexity - medium_cfg) * scoring[
            "complexity_medium_penalty_per_point"
        ]
    breakdown["complexity"] = -round(complexity_penalty, 2)

    # Deduct for worst-case complexity outliers (per-function gates care about
    # the maximum, not only the average).
    max_penalty = 0.0
    high_cfg = scoring["complexity_high_threshold"]
    if max_complexity > high_cfg:
        max_penalty = (max_complexity - high_cfg) * scoring[
            "complexity_high_penalty_per_point"
        ]
        max_penalty = min(max_penalty, scoring["complexity_high_penalty_cap"])
    breakdown["max_complexity"] = -round(max_penalty, 2)

    # Deduct for low maintainability.
    mi_penalty = 0.0
    mi_cfg = scoring["maintainability_threshold"]
    if avg_mi < mi_cfg:
        mi_penalty = (mi_cfg - avg_mi) * scoring["maintainability_penalty_per_point"]
    breakdown["maintainability"] = -round(mi_penalty, 2)

    # Bonus/Penalty for tests. A None count means "not evaluated", so no penalty.
    tests_adjustment = 0.0
    if test_files_count == 0 and total_loc > 0:
        tests_adjustment = -scoring["no_tests_penalty"]
    elif test_files_count:
        tests_adjustment = min(
            scoring["tests_bonus_cap"],
            test_files_count * scoring["tests_bonus_per_file"],
        )
    breakdown["tests"] = round(tests_adjustment, 2)

    score = max(0.0, min(100.0, sum(breakdown.values())))

    # QGIS specific adjustments
    extra_data = extra_data or {}
    qgis_data = extra_data.get("qgis_compliance", {})
    if qgis_data:
        # Example: penalize legacy imports
        pass

    return {
        metric_keys.QUALITY_SCORE: score,
        metric_keys.TOTAL_LINES_CODE: total_loc,
        metric_keys.TOTAL_PHYSICAL_LINES: total_physical,
        metric_keys.TOTAL_FUNCTIONS: total_functions,
        metric_keys.TOTAL_CLASSES: total_classes,
        metric_keys.AVERAGE_COMPLEXITY: round(avg_complexity, 2),
        metric_keys.MAX_COMPLEXITY: max_complexity,
        metric_keys.AVG_MAINTENANCE_INDEX: round(avg_mi, 2),
        metric_keys.TEST_FILES_COUNT: test_files_count,
        metric_keys.ENTRY_POINTS_COUNT: len(entry_points),
        metric_keys.SCORE_BREAKDOWN: breakdown,
    }
