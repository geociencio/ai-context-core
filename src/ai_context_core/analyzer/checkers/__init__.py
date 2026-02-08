"""Compatibility facade for checkers."""

from ..visitors.checker_base import BaseChecker
from ..visitors.security_checker import SecurityChecker
from ..visitors.tech_debt_checker import TechDebtChecker
from ..visitors.optimization_checker import OptimizationChecker

__all__ = [
    "BaseChecker",
    "SecurityChecker",
    "TechDebtChecker",
    "OptimizationChecker",
]
