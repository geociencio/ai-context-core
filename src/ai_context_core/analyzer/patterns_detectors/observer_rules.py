"""Specialized rules for detecting observer pattern indicators."""

import ast

from .observer_components import (
    detect_signals as _sig_detect,
    check_init_assign as _init_check,
    check_iteration as _iter_check,
    check_mgmt_method as _mgmt_check,
    check_notify_method as _notify_check
)

class ObserverRules:
    """Encapsulates patterns for observer detection.
    
    Delegates to specialized components to maintain low complexity.
    """

    @staticmethod
    def check_init_assign(node: ast.Assign) -> bool:
        """Checks if assignment is for an observer collection."""
        return _init_check(node)

    @staticmethod
    def check_mgmt_method(name: str) -> bool:
        """Checks if method name matches management patterns."""
        return _mgmt_check(name)

    @staticmethod
    def check_notify_method(name: str) -> bool:
        """Checks if method name matches notification patterns."""
        return _notify_check(name)

    @staticmethod
    def check_iteration(node: ast.AST) -> bool:
        """Checks for iteration over observer collections."""
        return _iter_check(node)

    @staticmethod
    def detect_signals(node: ast.AST) -> int:
        """Counts signal definitions."""
        return _sig_detect(node)
