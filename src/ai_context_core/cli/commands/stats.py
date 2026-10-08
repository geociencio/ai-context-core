"""Statistics command logic."""

import pathlib
import click
from rich.console import Console
from rich.table import Table
from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.analyzer.builders import metric_keys
from ai_context_core.analyzer.builders import formatter
from ai_context_core.config.loader import ConfigLoader


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

    table.add_row("Source Lines (SLOC)", f"{metrics.get(metric_keys.TOTAL_LINES_CODE, 0):,}")
    table.add_row("Physical Lines", f"{metrics.get(metric_keys.TOTAL_PHYSICAL_LINES, 0):,}")
    table.add_row("Modules", str(complexity.get(formatter.TOTAL_MODULES, 0)))
    table.add_row("Functions", str(complexity.get(formatter.TOTAL_FUNCTIONS, 0)))
    table.add_row("Classes", str(complexity.get(formatter.TOTAL_CLASSES, 0)))
    table.add_row(
        "Avg Cyclomatic Complexity",
        f"{complexity.get(formatter.AVERAGE_COMPLEXITY, 0):.1f}",
    )
    table.add_row(
        "Avg Maintenance Index",
        f"{complexity.get(formatter.AVG_MAINTENANCE_INDEX, 0):.1f}",
    )
    table.add_row("ai-ctx Quality Score", f"{metrics.get(metric_keys.QUALITY_SCORE, 0):.1f}/100")

    console.print(table)

    _show_complex_modules(complexity)


def _show_complex_modules(complexity):
    click.secho("\n🔴 Top 5 Most Complex Modules", fg="red", bold=True)
    complex_mods = complexity.get(formatter.MOST_COMPLEX_MODULES, [])[:5]
    if complex_mods:
        for mod, comp in complex_mods:
            click.echo(f"  - {mod}: {comp}")
