"""Initialization command logic."""

import pathlib
import shutil
import click
from ai_context_core.config.loader import ConfigLoader


def initialize_project(path: str, profile: str):
    """Sets up the initial project structure and configuration.

    Args:
        path: Target project path.
        profile: Configuration profile to use.
    """
    proj = pathlib.Path(path).resolve()
    ai_ctx, agent_wf = proj / ".ai-context", proj / ".agent" / "workflows"
    click.echo(f"🔄 Initializing {proj} with '{profile}'...")
    ai_ctx.mkdir(exist_ok=True)
    agent_wf.mkdir(parents=True, exist_ok=True)

    loader = ConfigLoader()
    if profile != "generic":
        p_path = loader.profiles_path / f"{profile}.yaml"
        if p_path.exists():
            shutil.copy2(p_path, ai_ctx / "config.yaml")

    templates = pathlib.Path(__file__).parent.parent / "templates"
    for wf in (templates / "workflows").glob("*.md"):
        dest = agent_wf / wf.name
        if not dest.exists():
            shutil.copy2(wf, dest)

    prompt_src = templates / "initial_prompt.md"
    prompt_dest = ai_ctx / "prompt_inicial.md"
    if prompt_src.exists() and not prompt_dest.exists():
        c = (
            prompt_src.read_text(encoding="utf-8")
            .replace("{project_name}", proj.name)
            .replace("{project_type}", profile)
        )
        prompt_dest.write_text(c, encoding="utf-8")
    click.secho("✨ Ready.", fg="green")
