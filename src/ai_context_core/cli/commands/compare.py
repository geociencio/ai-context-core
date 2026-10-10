"""Logic for the 'compare' command to track quality evolution."""

import json
import pathlib
import click
from typing import Dict, Any

from ai_context_core.analyzer.builders import metric_keys

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:

    class Console:
        def print(self, *args, **kwargs):
            print(*args)

    class Table:
        def __init__(self, *args, **kwargs):
            pass

        def add_column(self, *args, **kwargs):
            pass

        def add_row(self, *args, **kwargs):
            pass


console = Console()


def run_compare(file1: str, file2: str):
    """Compare two analysis JSON files."""
    p1 = pathlib.Path(file1)
    p2 = pathlib.Path(file2)

    if not p1.exists() or not p2.exists():
        click.secho(f"❌ One or both files do not exist: {file1}, {file2}", fg="red")
        return

    try:
        data1 = json.loads(p1.read_text(encoding="utf-8"))
        data2 = json.loads(p2.read_text(encoding="utf-8"))
    except Exception as e:
        click.secho(f"❌ Error parsing JSON: {e}", fg="red")
        return

    click.echo(f"📊 Comparing {p1.name} (Base) vs {p2.name} (Current)\n")

    table = Table(title="Regression Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Base", justify="right")
    table.add_column("Current", justify="right")
    table.add_column("Diff", justify="right")

    metrics_to_compare = [
        ("Quality Score (heuristic)", f"metrics.{metric_keys.QUALITY_SCORE}"),
        ("Maintenance Index", f"metrics.{metric_keys.AVG_MAINTENANCE_INDEX}"),
        ("Cyclomatic Complexity (Avg)", f"metrics.{metric_keys.AVERAGE_COMPLEXITY}"),
        ("Max Complexity", f"metrics.{metric_keys.MAX_COMPLEXITY}"),
        ("Total Lines", f"metrics.{metric_keys.TOTAL_LINES_CODE}"),
        ("Functions", f"metrics.{metric_keys.TOTAL_FUNCTIONS}"),
        ("Classes", f"metrics.{metric_keys.TOTAL_CLASSES}"),
        ("Modules", "structure.modules_count"),
    ]

    for label, path in metrics_to_compare:
        val1 = _get_nested(data1, path)
        val2 = _get_nested(data2, path)

        diff = 0
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            diff = val2 - val1

        diff_str = f"{diff:+.2f}" if isinstance(diff, float) else f"{diff:+d}"

        # Color logic (negative is bad for score, but bad for complexity)
        color = "white"
        if "Score" in label or "Index" in label:
            color = "green" if diff > 0 else "red" if diff < 0 else "white"
        elif "Complexity" in label or "Issues" in label:
            color = "red" if diff > 0 else "green" if diff < 0 else "white"

        table.add_row(label, str(val1), str(val2), f"[{color}]{diff_str}[/{color}]")

    console.print(table)


def _get_nested(data: Dict[str, Any], path: str) -> Any:
    """Helper to get nested dictionary values using dot notation."""
    keys = path.split(".")
    val = data
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k, 0)
        else:
            return 0
    return val
