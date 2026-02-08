"""Compatibility facade for observer rules."""

from ..visitors.observer_rules import (
    check_init_assign,
    check_iteration,
    check_mgmt_method,
    check_notify_method,
    detect_signals,
    _is_signal_definition,
    _check_connection_call,
    analyze_class_body,
)

__all__ = [
    "check_init_assign",
    "check_iteration",
    "check_mgmt_method",
    "check_notify_method",
    "detect_signals",
    "_is_signal_definition",
    "_check_connection_call",
    "analyze_class_body",
]
