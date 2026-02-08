"""Core metrics calculation logic (MI, Halstead, etc.)."""

import math
from typing import Dict, Any


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
    test_files_count: int,
    config: Dict[str, Any],
    extra_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Calculate aggregated project metrics.

    Args:
        modules: List of module analysis results.
        entry_points: List of entry point/main file paths.
        test_files_count: Number of test files found.
        config: Configuration dictionary.
        extra_data: Additional data like QGIS compliance results.

    Returns:
        Dictionary with aggregated project metrics.
    """
    total_loc = sum(m.get("sloc", m.get("loc", 0)) for m in modules)
    total_physical = sum(m.get("lines", 0) for m in modules)
    total_complexity = sum(m.get("complexity", 0) for m in modules)
    avg_complexity = total_complexity / len(modules) if modules else 0
    max_complexity = max((m.get("complexity", 0) for m in modules), default=0)

    # Calculate maintainability
    total_mi = sum(m.get("maintenance_index", 100) for m in modules)
    avg_mi = total_mi / len(modules) if modules else 100

    # Calculate Quality Score
    # Base score start at 100
    score = 100.0

    # Deduct for complexity
    if avg_complexity > config.get("thresholds", {}).get("complexity_medium", 15):
        score -= (avg_complexity - 15) * 2

    # Deduct for low maintainability
    if avg_mi < 65:
        score -= (65 - avg_mi) * 1.5

    # Bonus/Penalty for tests
    # Simple heuristic: if test_files_count is 0 and we have code -> penalty
    if test_files_count == 0 and total_loc > 0:
        score -= 20
    elif test_files_count > 0:
        score += min(10, test_files_count * 2)

    # QGIS specific adjustments
    extra_data = extra_data or {}
    qgis_data = extra_data.get("qgis_compliance", {})
    if qgis_data:
        # Example: penalize legacy imports
        pass

    return {
        "quality_score": max(0.0, min(100.0, score)),
        "total_lines_code": total_loc,
        "total_physical_lines": total_physical,
        "avg_complexity": round(avg_complexity, 2),
        "max_complexity": max_complexity,
        "avg_maintainability": round(avg_mi, 2),
        "test_files_count": test_files_count,
        "entry_points_count": len(entry_points),
    }
