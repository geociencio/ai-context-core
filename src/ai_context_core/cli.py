"""Command Line Interface for Ai-Context-Core."""

import click

from .cli_groups import ALL_CMDS


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

# Add aliases for backward compatibility if they differ from name
cli.add_command(ALL_CMDS[0], name="init_cmd")  # init_cmd alias
cli.add_command(ALL_CMDS[5], name="analyze_cmd")  # analyze_cmd alias
cli.add_command(ALL_CMDS[7], name="inspect_cmd")  # inspect_cmd alias
cli.add_command(ALL_CMDS[3], name="serve_cmd")  # serve_cmd alias
cli.add_command(ALL_CMDS[6], name="audit_cmd")  # audit_cmd alias
cli.add_command(ALL_CMDS[8], name="patterns_cmd")  # patterns_cmd alias
cli.add_command(ALL_CMDS[9], name="security_cmd")  # security_cmd alias
cli.add_command(ALL_CMDS[11], name="deps_cmd")  # deps_cmd alias
cli.add_command(ALL_CMDS[12], name="git_cmd")  # git_cmd alias
cli.add_command(ALL_CMDS[1], name="stats_cmd")  # stats_cmd alias
cli.add_command(ALL_CMDS[13], name="qgis_cmd")  # qgis_cmd alias
cli.add_command(ALL_CMDS[2], name="clean_cmd")  # clean_cmd alias

if __name__ == "__main__":
    cli()
