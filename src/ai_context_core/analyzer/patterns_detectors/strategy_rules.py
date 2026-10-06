"""Compatibility facade for strategy rules.

Deprecated: use ``ai_context_core.analyzer.visitors.strategy_rules`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.strategy_rules import StrategyRules

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.strategy_rules")

__all__ = ["StrategyRules"]
