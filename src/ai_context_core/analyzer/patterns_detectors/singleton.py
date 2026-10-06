"""Compatibility facade for singleton detector.

Deprecated: use ``ai_context_core.analyzer.visitors.singleton`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..visitors.singleton import detect_singleton

warn_deprecated(__name__, "ai_context_core.analyzer.visitors.singleton")

__all__ = ["detect_singleton"]
