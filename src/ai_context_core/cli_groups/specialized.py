"""Facade for legacy specialized commands.

Deprecated: use ``ai_context_core.cli.commands.specialized`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..cli.commands.specialized import qgis_cmd, git_cmd, deps_cmd  # noqa: F401

warn_deprecated(__name__, "ai_context_core.cli.commands.specialized")
