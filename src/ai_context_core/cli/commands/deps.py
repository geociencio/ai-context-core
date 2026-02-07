"""Dependency analysis command logic."""

import pathlib
import click
from rich.console import Console
from rich.table import Table
from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.config.loader import ConfigLoader


def show_dependencies(
    path: str, show_unused: bool, show_cycles: bool, show_metrics: bool
):
    """Shows dependency analysis results."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    res = analyzer.analyze()
    deps = res.get("dependencies", {})
    console = Console()

    if show_unused:
        _show_unused(deps)
    if show_cycles:
        _show_cycles(deps)
    if show_metrics:
        _show_metrics(deps, console)


def _show_unused(deps):
    click.secho("🗑️  UNUSED IMPORTS", fg="yellow", bold=True)
    unused = deps.get("unused_imports", {})
    if not unused:
        click.echo("No unused imports detected.")
    else:
        for module, imports in unused.items():
            click.echo(f"\n📄 {module}:")
            for imp in imports:
                click.echo(f"  - {imp}")


def _show_cycles(deps):
    click.secho("\n🔄 CIRCULAR DEPENDENCIES", fg="red", bold=True)
    cycles = deps.get("circular_dependencies", [])
    if not cycles:
        click.echo("No circular dependencies detected. ✅")
    else:
        for i, cycle in enumerate(cycles, 1):
            click.echo(f"{i}. {' → '.join(cycle)}")


def _show_metrics(deps, console):
    click.secho("\n📊 DEPENDENCY METRICS", fg="cyan", bold=True)
    metrics = deps.get("graph_metrics", {})
    coupling = deps.get("coupling_metrics", {})

    table = Table(title="Graph Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Nodes", str(metrics.get("nodes", 0)))
    table.add_row("Edges", str(metrics.get("edges", 0)))
    table.add_row("Density", f"{metrics.get('density', 0):.3f}")
    table.add_row("Is DAG", "✅" if metrics.get("is_dag") else "❌")
    table.add_row("Components", str(metrics.get("weakly_connected_components", 0)))

    console.print(table)

    if coupling:
        click.echo("\n🔗 Top 5 Most Coupled Modules:")
        sorted_coupling = sorted(
            coupling.items(), key=lambda x: x[1].get("cbo", 0), reverse=True
        )[:5]
        for mod, metrics_val in sorted_coupling:
            cbo = metrics_val.get("cbo", 0)
            click.echo(f"  - {mod}: CBO={cbo}")
