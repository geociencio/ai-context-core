"""Filter and report commands for the CLI (patterns, security, help-me)."""

import click
from ai_context_core.commands import report


@click.command(name="patterns")
@click.option("--path", default=".", help="Project path")
def patterns_cmd(path: str):
    """Shows only detected design patterns."""
    report.show_specific(path, "patterns")


@click.command(name="security")
@click.option("--path", default=".", help="Project path")
def security_cmd(path: str):
    """Shows only security issues."""
    report.show_specific(path, "security")


@click.command(name="help-me")
@click.option("--path", default=".", help="Project path")
def help_me_cmd(path: str):
    """Shows only AI recommendations."""
    report.show_specific(path, "recommendations")
