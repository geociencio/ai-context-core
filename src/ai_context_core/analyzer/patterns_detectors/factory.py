"""Compatibility facade for factory detector.

Deprecated: use ``ai_context_core.analyzer.visitors.factory`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.factory import detect_factory

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.factory")

__all__ = ["detect_factory"]
