"""Analysis commands for the CLI (analyze, audit, inspect)."""

import click
from typing import Optional
from ai_context_core.commands import analyze, inspect


@click.command(name="analyze")
@click.option("--path", default=".", help="Project path")
@click.option("--workers", "-w", default=None, type=int, help="Parallel workers")
@click.option(
    "--format", "-f", type=click.Choice(["markdown", "html"]), default="markdown"
)
@click.option("--no-cache", is_flag=True, help="Force full analysis, ignoring cache")
def analyze_cmd(path: str, workers: Optional[int], format: str, no_cache: bool):
    """Runs project analysis."""
    analyze.run_analysis(path, workers, format, no_cache)


@click.command(name="audit")
@click.option("--path", default=".", help="Project path")
@click.option(
    "--threshold", "-t", default=70.0, type=float, help="Minimum Quality Score"
)
def audit_cmd(path: str, threshold: float):
    """Fails if Quality Score is below threshold."""
    analyze.run_audit(path, threshold)


@click.command(name="inspect")
@click.argument("file_path")
def inspect_cmd(file_path: str):
    """Deep analysis of a single file."""
    inspect.inspect_file(file_path)
