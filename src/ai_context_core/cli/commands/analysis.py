"""Analysis commands for the CLI (analyze, context)."""

import click
from typing import Optional
from . import analyze


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
    "--source",
    type=click.Choice(["auto", "external", "builtin"]),
    default="auto",
    help="Analysis source: auto (external if present, else builtin), external, builtin",
)
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
    source: str,
    include_md: tuple,
):
    """Runs project analysis."""
    analyze.run_analysis(
        path, workers, format, no_cache, include_md=list(include_md), source=source
    )


@click.command(name="context")
@click.option("--path", default=".", help="Project path")
@click.option("--workers", "-w", default=None, type=int, help="Parallel workers")
@click.option("--no-cache", is_flag=True, help="Force full analysis, ignoring cache")
@click.option(
    "--source",
    type=click.Choice(["auto", "external", "builtin"]),
    default="auto",
    help="Analysis source: auto (external if present, else builtin), external, builtin",
)
@click.option(
    "--max-tokens",
    type=int,
    default=None,
    help="Global token cap for AI_CONTEXT.md (deterministic truncation)",
)
@click.option(
    "--check",
    "check",
    is_flag=True,
    help="Verify freshness after generating; exit 1 if stale (CI)",
)
@click.option(
    "--include-md",
    "include_md",
    multiple=True,
    help="Glob (relative to the project root) of extra markdown docs to embed; repeatable",
)
def context_cmd(
    path: str,
    workers: Optional[int],
    no_cache: bool,
    source: str,
    max_tokens: Optional[int],
    check: bool,
    include_md: tuple,
):
    """Generates AI_CONTEXT.md, project_context.json and context_manifest.json."""
    analyze.run_context(
        path,
        workers,
        no_cache,
        include_md=list(include_md),
        source=source,
        max_tokens=max_tokens,
        check=check,
    )
