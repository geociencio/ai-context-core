"""Initialization command logic."""

import pathlib
import shutil
import click


def initialize_project(path: str, profile: str):
    """Sets up the initial project structure and configuration.

    Args:
        path: Target project path.
        profile: Configuration profile to use.
    """
    proj = pathlib.Path(path).resolve()
    ai_ctx = proj / ".ai-context"
    click.echo(f"🔄 Initializing {proj} with '{profile}'...")
    ai_ctx.mkdir(exist_ok=True)

    pkg_root = pathlib.Path(__file__).parent.parent.parent
    profiles_dir = pkg_root / "config" / "profiles"
    if profile != "generic":
        # Prefer TOML profiles
        p_toml = profiles_dir / f"{profile}.toml"
        p_yaml = profiles_dir / f"{profile}.yaml"
        if p_toml.exists():
            shutil.copy2(p_toml, ai_ctx / "config.toml")
        elif p_yaml.exists():
            shutil.copy2(p_yaml, ai_ctx / "config.yaml")

    prompt_src = pkg_root / "templates" / "initial_prompt.md"
    prompt_dest = ai_ctx / "prompt_inicial.md"
    if prompt_src.exists() and not prompt_dest.exists():
        c = (
            prompt_src.read_text(encoding="utf-8")
            .replace("{project_name}", proj.name)
            .replace("{project_type}", profile)
        )
        prompt_dest.write_text(c, encoding="utf-8")

    click.echo(
        "ℹ️  Workflows are provided by the agentic-forge framework "
        "(mount `.agent/`); no workflow templates are scaffolded."
    )
    click.secho("✨ Ready.", fg="green")
