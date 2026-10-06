"""Compatibility facade for report commands.

Deprecated: use ``ai_context_core.cli.commands.report`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..cli.commands.report import (
    _show_patterns,
    _show_security,
    _show_recommendations,
)

warn_deprecated(__name__, "ai_context_core.cli.commands.report")

__all__ = ["_show_patterns", "_show_security", "_show_recommendations"]
