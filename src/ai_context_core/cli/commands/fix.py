"""Logic for the auto-remediation 'fix' command."""

import pathlib
import subprocess
import click
import sys


def run_fix(path: str, sync_version: bool = False):
    """Attempt to fix common project issues."""
    proj_path = pathlib.Path(path).resolve()
    click.echo(f"🛠️ Attempting to fix issues at: {proj_path}\n")

    # 1. Run Ruff Fix
    click.echo("🔍 Running Ruff check with --fix...")
    try:
        subprocess.run(
            ["uv", "run", "ruff", "check", ".", "--fix"], cwd=proj_path, check=False
        )
        click.echo("✅ Ruff fixes applied (if any).")
    except FileNotFoundError:
        click.echo("⚠️ 'uv' or 'ruff' not found. Skipping lint fixes.")

    # 2. Fix missing __init__.py in src subdirs
    src_dir = proj_path / "src"
    if src_dir.exists():
        for d in src_dir.iterdir():
            if (
                d.is_dir()
                and not (d / "__init__.py").exists()
                and not d.name.startswith(".")
                and d.name != "__pycache__"
            ):
                click.echo(f"📁 Creating missing __init__.py in {d.name}...")
                (d / "__init__.py").touch()
                click.echo(f"✅ Created {d.name}/__init__.py")

    # 3. Synchronize versions (if requested)
    if sync_version:
        synchronize_versions(proj_path)

    click.echo("\n✨ Fix process completed.")


def synchronize_versions(path: pathlib.Path):
    """Synchronize __init__.py version with pyproject.toml."""
    # This is a bit complex to do safely without a parser, but we can try simple regex/replace
    pyproject_file = path / "pyproject.toml"
    init_file = path / "src" / "ai_context_core" / "__init__.py"

    if not pyproject_file.exists() or not init_file.exists():
        click.echo("⚠️ Could not find both version files for synchronization.")
        return

    # Get version from pyproject.toml
    version = None
    try:
        if sys.version_info >= (3, 11):
            import tomllib

            with open(pyproject_file, "rb") as f:
                data = tomllib.load(f)
                version = data.get("project", {}).get("version")
        else:
            import tomli

            with open(pyproject_file, "rb") as f:
                data = tomli.load(f)
                version = data.get("project", {}).get("version")
    except Exception:
        pass

    if not version:
        click.echo("⚠️ Could not extract version from pyproject.toml.")
        return

    # Update __init__.py
    lines = init_file.read_text().splitlines()
    new_lines = []
    updated = False
    for line in lines:
        if line.startswith("__version__"):
            new_lines.append(f'__version__ = "{version}"')
            updated = True
        else:
            new_lines.append(line)

    if updated:
        init_file.write_text("\n".join(new_lines) + "\n")
        click.echo(f"✅ Synchronized __init__.py to version {version}")
    else:
        click.echo("⚠️ Could not find __version__ variable in __init__.py to update.")
