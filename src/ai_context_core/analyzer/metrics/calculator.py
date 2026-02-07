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
def calculate_maintenance_index(v: float, g: int, loc: int) -> float:
    """Standalone function to calculate Maintenance Index."""
    return MetricsCalculator.maintenance_index(v, g, loc)


def calculate_halstead_metrics(n1: int, n2: int, N1: int, N2: int) -> Dict[str, float]:
    """Standalone function to calculate Halstead metrics."""
    return MetricsCalculator.halstead_metrics(n1, n2, N1, N2)
