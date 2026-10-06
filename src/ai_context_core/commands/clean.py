"""Compatibility facade for clean command.

Deprecated: use ``ai_context_core.cli.commands.clean`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..cli.commands.clean import clean_artifacts

warn_deprecated(__name__, "ai_context_core.cli.commands.clean")

__all__ = ["clean_artifacts"]
