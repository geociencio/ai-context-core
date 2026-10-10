"""Maintenance commands for the CLI (graph, compare, roadmap)."""

import click
from . import graph, compare, roadmap


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


@click.command(name="roadmap")
@click.option("--path", default=".", help="Project path")
def roadmap_cmd(path: str):
    """Generate technical debt prioritization roadmap."""
    roadmap.run_roadmap(path)
