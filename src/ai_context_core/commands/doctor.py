"""Logic for the diagnostics 'doctor' command."""

import pathlib
import sys
import click
from typing import Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:

    class Console:
        def print(self, *args, **kwargs):
            print(*args)

    class Table:
        def __init__(self, *args, **kwargs):
            pass

        def add_column(self, *args, **kwargs):
            pass

        def add_row(self, *args, **kwargs):
            pass

    class Panel:
        def __init__(self, *args, **kwargs):
            pass


console = Console()


def run_doctor(path: str):
    """Run environmental diagnostics on the project."""
    proj_path = pathlib.Path(path).resolve()
    click.echo(f"🩺 Checking project at: {proj_path}\n")

    checks = [
        ("Version Consistency", check_versions(proj_path)),
        ("Config Files", check_configs(proj_path)),
        ("Python Environment", check_env()),
        ("Project Structure", check_structure(proj_path)),
    ]

    table = Table(title="Diagnostic Results")
    table.add_column("Category", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Message")

    all_ok = True
    for category, (status, msg) in checks:
        color = "green" if status == "OK" else "yellow" if status == "WARN" else "red"
        table.add_row(category, f"[{color}]{status}[/{color}]", msg)
        if status == "ERROR":
            all_ok = False

    console.print(table)

    if all_ok:
        console.print(
            "\n[bold green]Everything looks good! Keep coding! 🚀[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]Some issues were found. Use 'ai-ctx fix' to resolve common problems.[/bold red]"
        )


def check_versions(path: pathlib.Path) -> Tuple[str, str]:
    """Check version consistency between __init__.py and pyproject.toml."""
    init_version = "Unknown"
    pyproject_version = "Unknown"

    # Try __init__.py
    init_file = path / "src" / "ai_context_core" / "__init__.py"
    if init_file.exists():
        for line in init_file.read_text().splitlines():
            if "__version__" in line:
                init_version = line.split("=")[-1].strip().strip("'").strip('"')
                break

    # Try pyproject.toml
    pyproject_file = path / "pyproject.toml"
    if pyproject_file.exists():
        try:
            if sys.version_info >= (3, 11):
                import tomllib

                with open(pyproject_file, "rb") as f:
                    data = tomllib.load(f)
                    pyproject_version = data.get("project", {}).get(
                        "version", "Unknown"
                    )
            else:
                import tomli

                with open(pyproject_file, "rb") as f:
                    data = tomli.load(f)
                    pyproject_version = data.get("project", {}).get(
                        "version", "Unknown"
                    )
        except Exception:
            pass

    if init_version == pyproject_version:
        return "OK", f"Versions are consistent ({init_version})"
    if init_version == "Unknown" or pyproject_version == "Unknown":
        return (
            "WARN",
            f"Could not verify both versions (Init: {init_version}, Project: {pyproject_version})",
        )
    return (
        "ERROR",
        f"Version mismatch: __init__.py({init_version}) vs pyproject.toml({pyproject_version})",
    )


def check_configs(path: pathlib.Path) -> Tuple[str, str]:
    """Check for presence of mandatory configuration files."""
    required = [".ai-context", "pyproject.toml"]
    missing = [f for f in required if not (path / f).exists()]

    if not missing:
        return "OK", "Mandatory config files found."
    return "WARN", f"Missing suggested/mandatory files: {', '.join(missing)}"


def check_env() -> Tuple[str, str]:
    """Check Python version and environment."""
    v = sys.version_info
    if v.major == 3 and v.minor >= 9:
        return "OK", f"Python {v.major}.{v.minor}.{v.micro} is compatible."
    return (
        "WARN",
        f"Python {v.major}.{v.minor} might have compatibility issues (3.9+ recommended).",
    )


def check_structure(path: pathlib.Path) -> Tuple[str, str]:
    """Perform basic project structure checks."""
    src_dir = path / "src"
    if not src_dir.exists():
        return "WARN", "Standard 'src/' directory not found."

    # Check for __init__.py in first-level subdirs of src
    missing_init = []
    for d in src_dir.iterdir():
        if (
            d.is_dir()
            and not (d / "__init__.py").exists()
            and not d.name.startswith(".")
        ):
            missing_init.append(d.name)

    if missing_init:
        return "WARN", f"Missing __init__.py in: {', '.join(missing_init)}"

    return "OK", "Project structure looks standard."
