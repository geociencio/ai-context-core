"""Legacy compatibility wrappers for pattern detection."""

import ast
from typing import List, Dict, Any
from .singleton import SingletonDetector
from .factory import FactoryDetector
from .observer import ObserverDetector
from .strategy import StrategyDetector
from .decorator import DecoratorDetector


def detect_singleton(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects Singleton pattern occurrences."""
    return _detect_generic(tree, SingletonDetector())


def detect_factory(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects Factory pattern occurrences."""
    return _detect_generic(tree, FactoryDetector())


def detect_observer(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects Observer pattern occurrences."""
    return _detect_generic(tree, ObserverDetector())


def detect_strategy(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects Strategy pattern in the AST."""
    return _detect_generic(tree, StrategyDetector())


def detect_decorator(tree: ast.AST) -> List[Dict[str, Any]]:
    """Detects Decorator pattern in the AST."""
    return _detect_generic(tree, DecoratorDetector())


def _detect_generic(tree: ast.AST, detector) -> List[Dict[str, Any]]:
    """Generic detection helper for legacy wrappers."""
    res = []
    for node in ast.walk(tree):
        res.extend(detector.detect(node))
    return res
