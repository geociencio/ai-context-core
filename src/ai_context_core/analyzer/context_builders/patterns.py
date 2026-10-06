"""Compatibility facade for patterns context builder.

Deprecated: use ``ai_context_core.analyzer.builders.patterns`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..builders.patterns import PatternsBuilder

warn_deprecated(__name__, "ai_context_core.analyzer.builders.patterns")

__all__ = ["PatternsBuilder"]
