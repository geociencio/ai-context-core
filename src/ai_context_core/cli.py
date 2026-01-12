import click
import pathlib
import shutil
import os
from typing import Optional

from .analyzer.engine import ProjectAnalyzer
from .config.loader import ConfigLoader, list_profiles


@click.group()
def cli():
    """CLI tool for AI context management and project analysis."""
    pass


@cli.command()
@click.option(
    "--profile", "-p", help="Configuration profile (e.g. qgis-plugin)", default="generic"
)
@click.option("--path", default=".", help="Project path")
def init(profile: str, path: str):
    """Initializes the .ai-context structure in the project."""
    project_path = pathlib.Path(path).resolve()
    ai_context_dir = project_path / ".ai-context"
    agent_workflows_dir = project_path / ".agent" / "workflows"

    click.echo(f"🔄 Initializing AI Context in {project_path} with profile '{profile}'...")

    # 1. Crear directorios
    ai_context_dir.mkdir(exist_ok=True)
    agent_workflows_dir.mkdir(parents=True, exist_ok=True)

    # 2. Copiar/Generar Config
    loader = ConfigLoader()
    # Cargar config base del perfil para escribirla
    if profile != "generic":
        profile_path = loader.profiles_path / f"{profile}.yaml"
        if profile_path.exists():
            shutil.copy2(profile_path, ai_context_dir / "config.yaml")
            click.echo(f"✅ Profile configuration '{profile}' copied.")
        else:
            click.secho(
                f"⚠️ Profile '{profile}' not found. Using base configuration.", fg="yellow"
            )

    # 3. Copy Workflows
    templates_dir = pathlib.Path(__file__).parent / "templates" / "workflows"
    if templates_dir.exists():
        for wf in templates_dir.glob("*.md"):
            dest = agent_workflows_dir / wf.name
            if not dest.exists():
                shutil.copy2(wf, dest)
                click.echo(f"✅ Workflow installed: {wf.name}")
            else:
                click.echo(f"ℹ️ Workflow {wf.name} already exists. Skipping.")

    # 4. Copy Initial Prompt
    prompt_src = pathlib.Path(__file__).parent / "templates" / "initial_prompt.md"
    prompt_dest = ai_context_dir / "prompt_inicial.md"
    if prompt_src.exists() and not prompt_dest.exists():
        content = prompt_src.read_text(encoding="utf-8")
        # Replace basic placeholders
        content = content.replace("{project_name}", project_path.name)
        content = content.replace("{project_type}", profile)
        prompt_dest.write_text(content, encoding="utf-8")
        click.echo("✅ Initial prompt generated.")

    click.secho("✨ Initialization completed successfully.", fg="green")


@cli.command()
@click.option("--path", default=".", help="Path to the project")
@click.option("--workers", "-w", default=None, type=int, help="Number of parallel workers")
@click.option("--no-cache", is_flag=True, help="Disable cache")
def analyze(path: str, workers: Optional[int], no_cache: bool):
    """Runs project analysis and updates the context."""
    project_path = pathlib.Path(path).resolve()

    # Load configuration
    loader = ConfigLoader()

    # Try to detect profile or load local config
    local_config_path = project_path / ".ai-context" / "config.yaml"
    local_config = {}
    profile_name = None

    if local_config_path.exists():
        try:
            import yaml

            local_config = yaml.safe_load(local_config_path.read_text()) or {}
            profile_name = local_config.get("profile_name")
        except Exception:
            pass

    # Load final config
    config = loader.load_config(profile_name=profile_name, override_config=local_config)

    # Instantiate analyzer
    analyzer = ProjectAnalyzer(project_path=str(project_path), config=config, max_workers=workers)

    click.echo(f"🚀 Starting analysis for {project_path.name}...")

    try:
        results = analyzer.analyze()

        metrics = results.get("metrics", {})
        quality = metrics.get("quality_score", 0)

        click.echo("-" * 40)
        click.secho(
            f"🏆 Quality Score: {quality:.1f}/100", fg="green" if quality > 80 else "yellow"
        )
        click.echo(f"📊 Lines of Code: {metrics.get('total_lines_code', 0):,}")
        click.echo(f"💡 Optimizations: {len(results.get('optimizations', []))}")
        click.echo("-" * 40)
        click.secho("✅ Analysis completed and context updated.", fg="green")

    except Exception as e:
        click.secho(f"❌ Error during analysis: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        import sys

        sys.exit(1)


@cli.command()
def profiles():
    """Lists available configuration profiles."""
    click.echo("Available profiles:")
    for p in list_profiles():
        click.echo(f" - {p}")


if __name__ == "__main__":
    cli()
