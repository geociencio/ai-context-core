"""Report command for the CLI (context-health help-me)."""

import click
from . import report


@click.command(name="help-me")
@click.option("--path", default=".", help="Project path")
def help_me_cmd(path: str):
    """Shows context-health recommendations."""
    report.show_context_help(path)
