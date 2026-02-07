"""Cleaning command logic."""

import pathlib
import click


def clean_artifacts(path: str, dry_run: bool):
    """Cleans cache and generated artifacts."""
    proj = pathlib.Path(path).resolve()

    artifacts = [
        proj / ".ai_context_cache.json",
        proj / "AI_CONTEXT.md",
        proj / "project_context.json",
        proj / "PROJECT_SUMMARY.md",
        proj / "PROJECT_SUMMARY.html",
        proj / "ANALYSIS_REPORT.md",
    ]

    click.secho("🧹 CLEANING ARTIFACTS", fg="cyan", bold=True)

    deleted_count = 0
    for artifact in artifacts:
        if artifact.exists():
            if dry_run:
                click.echo(f"Would delete: {artifact.name}")
            else:
                artifact.unlink()
                click.secho(f"✅ Deleted: {artifact.name}", fg="green")
            deleted_count += 1

    if deleted_count == 0:
        click.echo("No artifacts found to clean.")
    elif dry_run:
        click.echo(
            f"\n{deleted_count} file(s) would be deleted. Run without --dry-run to delete."
        )
    else:
        click.secho(f"\n✨ Cleaned {deleted_count} file(s)", fg="green")
