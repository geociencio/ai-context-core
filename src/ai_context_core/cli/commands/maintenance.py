"""Maintenance commands for the CLI (doctor, fix, graph, compare, scaffold, roadmap)."""

import click
from . import doctor, fix, graph, compare, scaffold, roadmap


@click.group(name="maintenance")
def maintenance_group():
    """Project maintenance and exploration commands."""
    pass


@click.command(name="doctor")
@click.option("--path", default=".", help="Project path to diagnose")
def doctor_cmd(path: str):
    """Run diagnostics on the project environment."""
    doctor.run_doctor(path)


@click.command(name="fix")
@click.option("--path", default=".", help="Project path to fix")
@click.option(
    "--sync-version", is_flag=True, help="Synchronize __init__.py with pyproject.toml"
)
def fix_cmd(path: str, sync_version: bool):
    """Attempt to fix common project issues."""
    fix.run_fix(path, sync_version)


@click.command(name="graph")
@click.option("--path", default=".", help="Project path")
@click.option("--output", "-o", default="ARCHITECTURE.mmd", help="Output file name")
def graph_cmd(path: str, output: str):
    """Export architecture as Mermaid diagram."""
    graph.export_graph(path, output)


@click.command(name="compare")
@click.argument("file1")
@click.argument("file2")
def compare_cmd(file1: str, file2: str):
    """Compare two analysis results."""
    compare.run_compare(file1, file2)


@click.command(name="scaffold")
@click.argument("pattern")
@click.option("--output", "-o", help="Output file name")
def scaffold_cmd(pattern: str, output: str):
    """Generate code templates for design patterns."""
    scaffold.run_scaffold(pattern, output)


@click.command(name="roadmap")
@click.option("--path", default=".", help="Project path")
def roadmap_cmd(path: str):
    """Generate technical debt prioritization roadmap."""
    roadmap.run_roadmap(path)
