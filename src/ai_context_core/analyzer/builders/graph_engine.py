"""Internal engine for building and analyzing dependency graphs.

This module acts as a facade for the specialized graph analysis components.
"""

from .builder import ImportGraphBuilder
from .algorithms import CycleDetector, GraphMetricsCalculator

__all__ = ["ImportGraphBuilder", "CycleDetector", "GraphMetricsCalculator"]
