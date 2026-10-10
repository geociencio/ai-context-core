"""Logic for finding optimization opportunities."""

from typing import List, Dict, Any
from .optimization_checker import OptimizationChecker


def find_optimizations(
    modules_data: List[Dict[str, Any]], config: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """Find optimization opportunities in project modules.

    Args:
        modules_data: Analyzed module dictionaries.
        config: Analyzer configuration (``quality_thresholds``).

    Returns:
        Up to 30 optimization suggestions, one entry per affected module.
    """
    res = []
    checker = OptimizationChecker(config)
    for m in modules_data:
        sugs = checker.check(m)
        if sugs:
            res.append({"module": m["path"], "suggestions": sugs})
    return res[:30]
