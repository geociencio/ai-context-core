"""Inspection command logic."""

import pathlib
import sys
import click
from ..analyzer.engine import ProjectAnalyzer
from ..config.loader import ConfigLoader


def inspect_file(file_path: str):
    """Deep analysis of a single file."""
    path = pathlib.Path(file_path).resolve()
    if not path.exists() or not path.is_file():
        click.secho(f"❌ File not found: {file_path}", fg="red")
        sys.exit(1)

    loader = ConfigLoader()
    cfg = loader.load_config()
    # We need a ProjectAnalyzer to access its analysis methods
    analyzer = ProjectAnalyzer(project_path=str(path.parent), config=cfg)
    click.echo(f"🔍 Inspecting {path.name}...")

    data = analyzer._analyze_single_module(path)
    if data.get("syntax_error"):
        click.secho(f"❌ Syntax Error: {data.get('error')}", fg="red")
        sys.exit(1)

    click.echo("-" * 40)
    click.echo(f"📄 Module: {data['path']}")
    click.echo(f"📏 Lines: {data['lines']}")
    click.echo(f"📉 Complexity: {data['complexity']}")
    click.echo(f"🏗️  Patterns: {len(data.get('patterns', {}))}")
    click.echo(f"🔒 Security Issues: {len(data.get('ast_security', []))}")
    click.echo("-" * 40)
