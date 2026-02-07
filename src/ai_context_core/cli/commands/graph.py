"""Logic for the 'graph' command to export architectural diagrams."""

import pathlib
import click
from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.analyzer.reporting import generate_dependency_diagram
from ai_context_core.config.loader import ConfigLoader


def export_graph(path: str, output: str = "ARCHITECTURE.mmd"):
    """Export the project architecture as a Mermaid diagram."""
    proj_path = pathlib.Path(path).resolve()
    click.echo(f"📊 Generating dependency graph for: {proj_path.name}")

    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj_path), config=cfg)

    # We only need the dependency graph, but we run a full analysis for now
    # to reuse the existing pipeline. In the future, we could optimize this.
    res = analyzer.analyze()
    deps = res.get("dependencies", {})

    mermaid_code = generate_dependency_diagram(deps)

    if not mermaid_code:
        click.secho(
            "⚠️ Could not generate graph (no dependencies found or analyzed).",
            fg="yellow",
        )
        return

    output_path = proj_path / output
    output_path.write_text(mermaid_code, encoding="utf-8")

    click.secho(f"✅ Graph exported to {output_path.name}", fg="green")
    click.echo("💡 You can visualize this at https://mermaid.live/")
