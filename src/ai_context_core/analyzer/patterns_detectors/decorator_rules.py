"""Compatibility facade for decorator rules.

Deprecated: use ``ai_context_core.analyzer.visitors.decorator_rules`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.decorator_rules import DecoratorRules

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.decorator_rules")

__all__ = ["DecoratorRules"]
