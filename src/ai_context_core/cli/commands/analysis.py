"""Analysis commands for the CLI (analyze, audit, inspect)."""

import click
from typing import Optional
from . import analyze, inspect


@click.command(name="analyze")
@click.option("--path", default=".", help="Project path")
@click.option("--workers", "-w", default=None, type=int, help="Parallel workers")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["markdown", "html", "json"]),
    default="markdown",
)
@click.option("--no-cache", is_flag=True, help="Force full analysis, ignoring cache")
@click.option(
    "--include-md",
    "include_md",
    multiple=True,
    help="Glob (relative to the project root) of extra markdown docs to embed; repeatable",
)
def analyze_cmd(
    path: str,
    workers: Optional[int],
    format: str,
    no_cache: bool,
    include_md: tuple,
):
    """Runs project analysis."""
    analyze.run_analysis(path, workers, format, no_cache, include_md=list(include_md))


@click.command(name="audit")
@click.option("--path", default=".", help="Project path")
@click.option(
    "--threshold", "-t", default=70.0, type=float, help="Minimum ai-ctx Quality Score"
)
def audit_cmd(path: str, threshold: float):
    """Fails if ai-ctx Quality Score is below threshold."""
    analyze.run_audit(path, threshold)


@click.command(name="inspect")
@click.argument("file_path")
def inspect_cmd(file_path: str):
    """Deep analysis of a single file."""
    inspect.inspect_file(file_path)
