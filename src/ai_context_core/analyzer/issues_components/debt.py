"""Logic for finding technical debt."""

from typing import List, Dict, Any
from ..checkers.tech_debt_checker import TechDebtChecker

def find_technical_debt(modules_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find technical debt in project modules."""
    res = []
    checker = TechDebtChecker({})
    for m in modules_data:
        issues_found = checker.check(m)
        if issues_found:
            score = sum(
                3 if i["severity"] == "high" else 2 if i["severity"] == "medium" else 1
                for i in issues_found
            )
            res.append(
                {
                    "module": m["path"],
                    "issues": issues_found,
                    "total_issues": len(issues_found),
                    "severity_score": score,
                }
            )
    return sorted(res, key=lambda x: x["severity_score"], reverse=True)[:50]
