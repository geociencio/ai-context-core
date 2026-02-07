"""Statistics command logic."""

import pathlib
import click
from rich.console import Console
from rich.table import Table
from ..analyzer.engine import ProjectAnalyzer
from ..config.loader import ConfigLoader


def show_quick_stats(path: str):
    """Shows quick project statistics."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    res = analyzer.analyze()
    console = Console()

    metrics = res.get("metrics", {})
    complexity = res.get("complexity", {})

    click.secho("📊 PROJECT STATISTICS", fg="cyan", bold=True)
    table = Table(title=f"Summary for {proj.name}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")

    table.add_row("Source Lines (SLOC)", f"{metrics.get('total_lines_code', 0):,}")
    table.add_row("Physical Lines", f"{metrics.get('total_physical_lines', 0):,}")
    table.add_row("Modules", str(complexity.get("total_modules", 0)))
    table.add_row("Functions", str(complexity.get("total_functions", 0)))
    table.add_row("Classes", str(complexity.get("total_classes", 0)))
    table.add_row("Avg Complexity", f"{complexity.get('average_complexity', 0):.1f}")
    table.add_row(
        "Avg Maintenance Index", f"{complexity.get('avg_maintenance_index', 0):.1f}"
    )
    table.add_row("Quality Score", f"{metrics.get('quality_score', 0):.1f}/100")

    console.print(table)

    _show_complex_modules(complexity)


def _show_complex_modules(complexity):
    click.secho("\n🔴 Top 5 Most Complex Modules", fg="red", bold=True)
    complex_mods = complexity.get("most_complex_modules", [])[:5]
    if complex_mods:
        for mod, comp in complex_mods:
            click.echo(f"  - {mod}: {comp}")
