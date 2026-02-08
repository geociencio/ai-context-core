"""Compatibility facade for commands package.

Re-exports commands from ai_context_core.cli.commands.
"""

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
