"""Base commands for the CLI (init, stats, clean, serve, profiles)."""

import click
from ai_context_core.commands import init, stats, clean, serve
from ai_context_core.config.loader import list_profiles


@click.command(name="init")
@click.option("--profile", "-p", default="generic", help="Config profile")
@click.option("--path", default=".", help="Project path")
def init_cmd(profile: str, path: str):
    """Initializes the .ai-context structure."""
    init.initialize_project(path, profile)


@click.command(name="stats")
@click.option("--path", default=".", help="Project path")
def stats_cmd(path: str):
    """Shows quick project statistics."""
    stats.show_quick_stats(path)


@click.command(name="clean")
@click.option("--path", default=".", help="Project path")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be deleted without deleting"
)
def clean_cmd(path: str, dry_run: bool):
    """Cleans cache and generated artifacts."""
    clean.clean_artifacts(path, dry_run)


@click.command(name="serve")
@click.option("--port", "-p", default=8000, help="Server port")
@click.option("--open", "open_browser", is_flag=True, help="Open browser automatically")
def serve_cmd(port: int, open_browser: bool):
    """Serves the HTML report locally."""
    serve.start_server(port, open_browser)


@click.command(name="profiles")
def profiles_cmd():
    """Lists available profiles."""
    for p in list_profiles():
        click.echo(f" - {p}")
