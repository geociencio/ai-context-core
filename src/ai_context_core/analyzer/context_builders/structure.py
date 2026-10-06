"""Compatibility facade for structure context builder.

Deprecated: use ``ai_context_core.analyzer.builders.structure`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..builders.structure import StructureBuilder

warn_deprecated(__name__, "ai_context_core.analyzer.builders.structure")

__all__ = ["StructureBuilder"]
