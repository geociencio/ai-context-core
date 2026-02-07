"""Registry for issue checkers."""

from typing import List, Dict, Any, Type
from ..checkers import BaseChecker
from ..checkers.security_checker import SecurityChecker
from ..checkers.tech_debt_checker import TechDebtChecker
from ..checkers.optimization_checker import OptimizationChecker

class CheckerRegistry:
    """Registry for issue checkers."""

    _checkers: List[Type[BaseChecker]] = [
        SecurityChecker,
        TechDebtChecker,
        OptimizationChecker,
    ]

    @classmethod
    def register(cls, checker_cls: Type[BaseChecker]):
        """Registers a new checker class."""
        cls._checkers.append(checker_cls)

    @classmethod
    def run_all(
        cls, module_info: Dict[str, Any], config: Dict[str, Any] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Runs all registered checkers on the given module."""
        results = {}
        for checker_cls in cls._checkers:
            checker = checker_cls(config)
            issues_found = checker.check(module_info)
            if issues_found:
                cat = checker.get_category()
                if cat not in results:
                    results[cat] = []
                results[cat].extend(issues_found)
        return results
