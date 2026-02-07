"""Logic for finding optimization opportunities."""

from typing import List, Dict, Any
from ..checkers.optimization_checker import OptimizationChecker

def find_optimizations(modules_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find optimization opportunities in project modules."""
    res = []
    checker = OptimizationChecker()
    for m in modules_data:
        sugs = checker.check(m)
        if sugs:
            res.append({"module": m["path"], "suggestions": sugs})
    return res[:30]
