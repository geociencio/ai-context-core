"""Patterns components package."""

from .visitor import PatternsUnifiedVisitor
from .legacy import (
    detect_singleton,
    detect_factory,
    detect_observer,
    detect_strategy,
    detect_decorator,
)

__all__ = [
    "PatternsUnifiedVisitor",
    "detect_singleton",
    "detect_factory",
    "detect_observer",
    "detect_strategy",
    "detect_decorator",
]
