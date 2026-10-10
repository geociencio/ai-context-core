"""Hidden redirect stubs for commands removed in the v5.0.0 context-only contract.

These stubs keep the removed command names invocable for one deprecation cycle;
they print where the capability now lives and exit 0 so existing pipelines are
not broken outright. They are hidden from ``ai-ctx --help``.
"""

from typing import List

import click

_REDIRECTS = {
    "audit": "quality gates moved to qgis-plugin-analyzer (or 'ai-ctx health' in v5.0.0).",
    "inspect": "single-file analysis moved to qgis-plugin-analyzer.",
    "qgis": "QGIS compliance moved to qgis-plugin-analyzer.",
    "security": "security scanning moved to qgis-plugin-analyzer (+ bandit / detect-secrets).",
    "patterns": "design-pattern detection moved to qgis-plugin-analyzer.",
    "fix": "auto-remediation moved to qgis-plugin-analyzer.",
    "scaffold": "code scaffolding moved to agentic-forge.",
    "doctor": "environment diagnostics become 'ai-ctx health' in v5.0.0.",
    "interactive": "the interactive dashboard was removed in v5.0.0.",
    "serve": "HTML dashboards are owned by qgis-plugin-analyzer.",
    "full-scan": "use 'ai-ctx context' (single context path).",
}


def _make_redirect(name: str, message: str):
    """Build a hidden no-op command that prints a redirect notice.

    The command accepts (and ignores) any arguments so existing invocations with
    flags such as ``--threshold`` or ``--path`` keep working during the cycle.
    """

    @click.command(
        name=name,
        hidden=True,
        help=f"Deprecated: {message}",
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def _cmd(args: tuple):
        click.secho(f"'{name}' was removed in ai-context-core v5.0.0.", fg="yellow", err=True)
        click.secho(f"  -> {message}", fg="yellow", err=True)

    _cmd.__name__ = f"{name.replace('-', '_')}_redirect"
    return _cmd


DEPRECATED_CMDS: List[click.Command] = [
    _make_redirect(name, message) for name, message in _REDIRECTS.items()
]
