"""Compatibility facade for commands package.

Deprecated: use ``ai_context_core.cli.commands`` instead.
"""

from ai_context_core.deprecations import warn_deprecated

from ..cli.commands import (
    git,
    serve,
    analyze,
    deps,
    qgis,
    clean,
    init,
    inspect,
    report,
    doctor,
    fix,
)

warn_deprecated(__name__, "ai_context_core.cli.commands")

__all__ = [
    "git",
    "serve",
    "analyze",
    "deps",
    "qgis",
    "clean",
    "init",
    "inspect",
    "report",
    "doctor",
    "fix",
]
