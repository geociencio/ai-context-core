"""Logic for the 'roadmap' command to prioritize refactoring."""

import pathlib
import click
from ..analyzer.engine import ProjectAnalyzer
from ..config.loader import ConfigLoader

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


def run_roadmap(path: str):
    """Generate a refactoring roadmap based on complexity and churn."""
    proj_path = pathlib.Path(path).resolve()
    click.echo(f"🛣️  Generating refactoring roadmap for: {proj_path.name}")

    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj_path), config=cfg)

    res = analyzer.analyze()
    modules = res.get("modules", [])
    git_data = res.get("git", {})
    churn_data = {
        item["path"]: item["commits"] for item in git_data.get("hotspots", [])
    }

    # Calculate Refactor Score
    priorities = []
    for mod in modules:
        if mod.get("syntax_error"):
            continue

        path_str = mod["path"]
        complexity_data = mod.get("complexity", 0)
        if isinstance(complexity_data, dict):
            complexity = complexity_data.get("total_complexity", 0)
        else:
            complexity = complexity_data
        churn = churn_data.get(path_str, 1)  # Default to 1 if not in hotspots

        score = complexity * churn
        priorities.append(
            {"path": path_str, "complexity": complexity, "churn": churn, "score": score}
        )

    # Sort by score DESC
    priorities.sort(key=lambda x: x["score"], reverse=True)

    table = Table(title="Refactoring Roadmap (Top Priorities)")
    table.add_column("File", style="cyan")
    table.add_column("Complexity", justify="right")
    table.add_column("Churn", justify="right")
    table.add_column("Refactor Score", justify="right", style="bold magenta")

    for item in priorities[:15]:
        table.add_row(
            item["path"],
            str(item["complexity"]),
            str(item["churn"]),
            f"{item['score']:.1f}",
        )

    console.print(table)
    click.echo("\n💡 Priorities are calculated as (Complexity × Churn Frequency).")
