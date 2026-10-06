"""Compatibility facade for observer rules.

Deprecated: use ``ai_context_core.analyzer.visitors.observer_rules`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

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

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.observer_rules")

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
