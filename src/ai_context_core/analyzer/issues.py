"""Static analysis tools for identifying technical debt and security risks.

Includes rule-based detection for complexity hotspots, large modules,
security patterns, and optimization opportunities.

This module now uses a plugin-based system with Checkers.
"""

import pathlib
import warnings
from typing import List, Dict, Any, Type

from .checkers import BaseChecker
from .checkers.security_checker import SecurityChecker
from .checkers.tech_debt_checker import TechDebtChecker
from .checkers.optimization_checker import OptimizationChecker

# For backward compatibility, expose the ASTSecurityDetector class
# This is physically located here or imported from checkers if we moved it.
# In the refactoring plan, ASTSecurityDetector logic is inside SecurityChecker.
# However, to avoid breaking imports, we can define a proxy or keep the class.
# Given the previous step, ASTSecurityDetector was in issues.py.
# To cleanly separate, we should have moved ASTSecurityDetector to a utils file or inside the checker.
# For now, let's keep ASTSecurityDetector as a standalone class here for compatibility,
# but make it use the new logic if possible, or just keep it as legacy.
# BETTER APPROACH: Re-implement ASTSecurityDetector here as a wrapper or keep it as is
# but mark as part of the new system.
# ACTUALLY: The plan was "Migrar detectores existentes a clases individuales".
# So ASTSecurityDetector logic is now in SecurityChecker.
# We will alias it or re-define it to delegate if needed, or better yet,
# since this is an internal class, we might just keep it for now if external code uses it.
# Let's keep a minimal version or alias.
from .secrets import detect_secrets


class IssueDetector:
    """Base class for issue detection rules (Legacy)."""

    def detect(self, **kwargs) -> List[Dict[str, Any]]:
        raise NotImplementedError


# --- Checker Registry and Main Interface ---


class CheckerRegistry:
    """Registry for issue checkers."""

    _checkers: List[Type[BaseChecker]] = [
        SecurityChecker,
        TechDebtChecker,
        OptimizationChecker,
    ]

    @classmethod
    def register(cls, checker_cls: Type[BaseChecker]):
        cls._checkers.append(checker_cls)

    @classmethod
    def run_all(
        cls, module_info: Dict[str, Any], config: Dict[str, Any] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        results = {}
        for checker_cls in cls._checkers:
            # Instantiate checker with configuration matching the interface
            checker = checker_cls(config)

            issues = checker.check(module_info)
            if issues:
                cat = checker.get_category()
                if cat not in results:
                    results[cat] = []
                results[cat].extend(issues)
        return results


# --- Public API Functions (Legacy Wrappers & New API) ---


def run_analysis(
    module_info: Dict[str, Any], config: Dict[str, Any] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Run all registered checkers on a module."""
    return CheckerRegistry.run_all(module_info, config)


def find_technical_debt(modules_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find technical debt in project modules."""
    res = []
    checker = TechDebtChecker({})
    for m in modules_data:
        issues = checker.check(m)
        if issues:
            # Calculate simplified score for legacy compatibility
            score = sum(
                3 if i["severity"] == "high" else 2 if i["severity"] == "medium" else 1
                for i in issues
            )
            res.append(
                {
                    "module": m["path"],
                    "issues": issues,
                    "total_issues": len(issues),
                    "severity_score": score,
                }
            )
    return sorted(res, key=lambda x: x["severity_score"], reverse=True)[:50]


def find_optimizations(modules_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find optimization opportunities in project modules."""
    res = []
    checker = OptimizationChecker()
    for m in modules_data:
        sugs = checker.check(m)
        if sugs:
            res.append({"module": m["path"], "suggestions": sugs})
    return res[:30]


def find_secrets(
    modules_data: List[Dict[str, Any]], project_path: str
) -> List[Dict[str, Any]]:
    """Scan project modules for exposed secrets."""
    # We can use the SecurityChecker mechanism or keep this standalone as per plan
    # The SecurityChecker also implements secret detection if content is passed.
    # To avoid logic duplication, we can use the checker, but we need to read files here.

    # Or keep the implementation I just added in the previous step, which is fine for now
    # to minimize risk.

    res = []
    base = pathlib.Path(project_path)
    for m in modules_data:
        path = m.get("path")
        if not path:
            continue
        try:
            with open(base / path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            issues = detect_secrets(content)
            if issues:
                severities = {"critical": 4, "high": 3, "medium": 2, "low": 1}
                max_sev_score = max(
                    (severities.get(i.get("severity", "low"), 0) for i in issues),
                    default=0,
                )
                max_sev_label = next(
                    (k for k, v in severities.items() if v == max_sev_score), "low"
                )

                res.append(
                    {
                        "module": path,
                        "issues": issues,
                        "total_issues": len(issues),
                        "max_severity": max_sev_label,
                    }
                )
        except Exception:
            continue
    return res


def find_security_issues(
    modules_data: List[Dict[str, Any]], project_path: str
) -> List[Dict[str, Any]]:
    """Find security issues in project modules (DEPRECATED)."""
    warnings.warn(
        "find_security_issues is deprecated. Use find_secrets or AST detection.",
        DeprecationWarning,
        stacklevel=2,
    )
    # Redirect to secrets detection as a best-effort fallback for existing consumers
    return find_secrets(modules_data, project_path)
