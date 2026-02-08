"""Compatibility facade for report commands."""

from ..cli.commands.report import (
    _show_patterns,
    _show_security,
    _show_recommendations,
)

__all__ = ["_show_patterns", "_show_security", "_show_recommendations"]
