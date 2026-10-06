"""Compatibility facade for decorator detector.

Deprecated: use ``ai_context_core.analyzer.visitors.decorator`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.decorator import detect_decorator

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.decorator")

__all__ = ["detect_decorator"]
