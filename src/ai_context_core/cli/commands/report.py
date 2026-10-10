"""Context-health recommendations for the ``help-me`` command."""

import pathlib

import click


def show_context_help(path: str) -> None:
    """Print context-oriented recommendations for a project.

    Args:
        path: Project root to analyze.
    """
    from ai_context_core.analyzer.engine import ProjectAnalyzer

    proj = pathlib.Path(path).resolve()
    res = ProjectAnalyzer(str(proj)).collect()

    click.secho("CONTEXT RECOMMENDATIONS", fg="cyan", bold=True)
    for tip in _recommendations(res):
        click.echo(f"- {tip}")


def _recommendations(res: dict) -> list:
    """Derive context-health tips from an analysis payload."""
    tips = []

    if not (res.get("manual_notes") or ""):
        tips.append(
            "Add .ai-context/architecture_notes.md (or project_brain.md) so the "
            "context carries curated architecture guidance, not just extracted facts."
        )

    git = res.get("git") or {}
    if not git.get("is_repo"):
        tips.append("No git history detected; churn/hotspot context will be empty.")

    if not (res.get("structure") or {}).get("tree"):
        tips.append("No structure tree generated; check the analysis scope.")

    if not tips:
        tips.append(
            "Context looks healthy. Regenerate after significant changes with 'ai-ctx context'."
        )
    return tips
