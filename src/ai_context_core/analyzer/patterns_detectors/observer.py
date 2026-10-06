"""Compatibility facade for observer detector.

Deprecated: use ``ai_context_core.analyzer.visitors.observer`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.observer import detect_observer

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.observer")

__all__ = ["detect_observer"]
