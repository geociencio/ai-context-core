"""Command Line Interface for Ai-Context-Core."""

import click

from .commands import ALL_CMDS


@click.group()
@click.version_option(package_name="ai-context-core")
def cli():
    """CLI tool for AI context management.

    Provides commands for analysis, design patterns, security and QGIS compliance.
    """
    pass


# Register all commands from fragmented groups
for cmd in ALL_CMDS:
    cli.add_command(cmd)


if __name__ == "__main__":
    cli()
