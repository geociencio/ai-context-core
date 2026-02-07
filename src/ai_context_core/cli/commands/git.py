"""Git evolution command logic."""

import pathlib
import sys
import click
from rich.console import Console
from rich.table import Table
from ai_context_core.analyzer import git_analysis


def show_git_evolution(path: str, days: int):
    """Shows git evolution analysis."""
    proj = pathlib.Path(path).resolve()
    analyzer = git_analysis.GitAnalyzer(proj)
    console = Console()

    if not analyzer.is_repo():
        click.secho("❌ Not a git repository", fg="red")
        sys.exit(1)

    _show_hotspots(analyzer, console)
    _show_churn(analyzer, days)


def _show_hotspots(analyzer, console):
    click.secho("🔥 GIT HOTSPOTS (Most Modified Files)", fg="red", bold=True)
    hotspots = analyzer.get_hotspots(limit=10)
    if not hotspots:
        click.echo("No hotspots found.")
    else:
        table = Table()
        table.add_column("File", style="cyan")
        table.add_column("Commits", style="yellow", justify="right")
        for h in hotspots:
            table.add_row(h["path"], str(h["commits"]))
        console.print(table)


def _show_churn(analyzer, days):
    click.secho(f"\n📈 CODE CHURN (Last {days} days)", fg="yellow", bold=True)
    churn = analyzer.get_churn(days=days)
    if not churn.get("available"):
        click.echo("No churn data available.")
    else:
        click.echo(f"Files Changed: {churn.get('files_changed', 0)}")
        click.echo(f"Lines Added: {churn.get('added', 0):,}")
        click.echo(f"Lines Deleted: {churn.get('deleted', 0):,}")
        click.echo(f"Total Churn: {churn.get('total_churn', 0):,}")
