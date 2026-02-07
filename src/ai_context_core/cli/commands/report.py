"""Reporting and recommendations command logic."""

import pathlib
import click
from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.config.loader import ConfigLoader


def show_specific(path: str, category: str):
    """Shows specific analysis category results."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    res = analyzer.analyze()

    if category == "patterns":
        _show_patterns(res)
    elif category == "security":
        _show_security(res)
    elif category == "recommendations":
        _show_recommendations(res)


def _show_patterns(res):
    click.secho("🏗️  DETECTED PATTERNS", fg="cyan", bold=True)
    pats = res.get("patterns", {})
    if not pats:
        click.echo("No patterns detected.")
    for name, occs in pats.items():
        for o in occs:
            class_name = o.get("class", o.get("name", "N/A"))
            module_path = o.get("module", "N/A")
            confidence = o.get("confidence", 0)
            click.echo(f"- {name}: {class_name} in {module_path} ({confidence}%)")


def _show_security(res):
    click.secho("🚨 SECURITY ISSUES", fg="red", bold=True)
    sec = res.get("security", [])
    if not sec:
        click.echo("No issues found.")
    for mod in sec:
        for issue in mod.get("issues", []):
            severity = issue.get("severity", "unknown").upper()
            module_name = mod.get("module", "N/A")
            message = issue.get("message", issue.get("description", "No description"))
            click.echo(f"- [{severity}] {module_name}: {message}")


def _show_recommendations(res):
    click.secho("💡 AI RECOMMENDATIONS", fg="yellow", bold=True)
    opts = res.get("optimizations", [])
    if not opts:
        click.echo("No recommendations.")
    for o in opts:
        module_name = o.get("module", "N/A")
        for sug in o.get("suggestions", []):
            message = sug.get("message", "N/A")
            click.echo(f"- [{module_name}] {message}")
