"""Command Line Interface for Ai-Context-Core."""

import click

from .commands import ALL_CMDS


@click.group()
@click.version_option(package_name="ai-context-core")
def cli():
    """CLI for compiling token-efficient, verifiable AI context.

    Context-only (v5.0.0): sources -> transform -> render -> verify.
    """
    pass


# Register all commands from fragmented groups
for cmd in ALL_CMDS:
    cli.add_command(cmd)


if __name__ == "__main__":
    cli()
