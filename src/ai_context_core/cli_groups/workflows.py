"""Facade for legacy workflows commands.

Deprecated: use ``ai_context_core.cli.commands.workflows`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..cli.commands.workflows import full_scan_cmd  # noqa: F401

warn_deprecated(__name__, "ai_context_core.cli.commands.workflows")
