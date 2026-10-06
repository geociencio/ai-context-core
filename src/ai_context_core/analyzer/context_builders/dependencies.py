"""Compatibility facade for dependency context builder.

Deprecated: use ``ai_context_core.analyzer.builders.dependencies`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..builders.dependencies import DependencyBuilder

warn_deprecated(__name__, "ai_context_core.analyzer.builders.dependencies")

__all__ = ["DependencyBuilder"]
