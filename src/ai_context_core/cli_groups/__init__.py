"""Facade for legacy CLI groups.

Deprecated: use ``ai_context_core.cli.commands`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

warn_deprecated(__name__, "ai_context_core.cli.commands")
