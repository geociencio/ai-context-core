"""Compatibility facade for patterns detectors base.

Deprecated: use ``ai_context_core.analyzer.pattern_base`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..pattern_base import PatternDetector

warn_deprecated(__name__, "ai_context_core.analyzer.pattern_base")

__all__ = ["PatternDetector"]
