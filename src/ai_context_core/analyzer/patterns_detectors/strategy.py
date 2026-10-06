"""Compatibility facade for strategy detector.

Deprecated: use ``ai_context_core.analyzer.visitors.strategy`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.strategy import detect_strategy

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.strategy")

__all__ = ["detect_strategy"]
