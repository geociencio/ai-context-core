"""Compatibility facade for singleton rules.

Deprecated: use ``ai_context_core.analyzer.visitors.singleton_rules`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.singleton_rules import (
    _is_singleton_instance_var,
    _check_singleton_new,
    _check_singleton_get_instance,
    check_singleton_method,
)

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.singleton_rules")

__all__ = [
    "_is_singleton_instance_var",
    "_check_singleton_new",
    "_check_singleton_get_instance",
    "check_singleton_method",
]
