"""Specialized commands for the CLI (deps, git, qgis)."""

import click
from . import deps, git, qgis


@click.command(name="deps")
@click.option("--path", default=".", help="Project path")
@click.option("--unused", is_flag=True, help="Show unused imports")
@click.option("--cycles", is_flag=True, help="Show circular dependencies")
@click.option("--metrics", is_flag=True, help="Show coupling metrics")
def deps_cmd(path: str, unused: bool, cycles: bool, metrics: bool):
    """Analyzes project dependencies."""
    if not (unused or cycles or metrics):
        unused = cycles = metrics = True
    deps.show_dependencies(path, unused, cycles, metrics)


@click.command(name="git")
@click.option("--path", default=".", help="Project path")
@click.option("--days", "-d", default=30, type=int, help="Days for churn analysis")
def git_cmd(path: str, days: int):
    """Shows git evolution analysis (hotspots and churn)."""
    git.show_git_evolution(path, days)


@click.command(name="qgis")
@click.option("--path", default=".", help="Project path")
def qgis_cmd(path: str):
    """Validates QGIS plugin compliance."""
    qgis.validate_qgis(path)
