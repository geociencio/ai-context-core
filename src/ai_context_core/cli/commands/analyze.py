"""Analysis and audit command logic."""

import os
import pathlib
import sys
from typing import Optional

import click

from ai_context_core.analyzer.builders import metric_keys
from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.analyzer.providers.config_loader import load_config


def run_analysis(
    path: str,
    workers: Optional[int],
    format: str,
    no_cache: bool,
    include_md: Optional[list] = None,
):
    """Executes the full project analysis pipeline."""
    proj = pathlib.Path(path).resolve()
    cfg = load_config(proj)
    analyzer = ProjectAnalyzer(
        project_path=str(proj),
        config=cfg,
        max_workers=workers,
        ignore_cache=no_cache,
        include_md=include_md,
    )
    if format != "json":
        click.echo(f"🚀 Analyzing {proj.name}...")
    try:
        res = analyzer.analyze(output_format=format)
        if format == "json":
            import json

            click.echo(json.dumps(res, indent=2, ensure_ascii=False))
            return

        m = res.get("metrics", {})
        q = m.get(metric_keys.QUALITY_SCORE, 0)
        click.echo("-" * 40)
        click.secho(
            f"🏆 ai-ctx Quality Score (heuristic): {q:.1f}/100",
            fg="green" if q > 80 else "yellow",
        )
        click.echo(
            f"📊 Lines: {m.get(metric_keys.TOTAL_LINES_CODE, 0):,}\n💡 Opts: {len(res.get('optimizations', []))}"
        )
        click.echo("-" * 40)
        click.secho("✅ Completed.", fg="green")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        sys.exit(1)


def run_context(
    path: str,
    workers: Optional[int],
    no_cache: bool,
    include_md: Optional[list] = None,
):
    """Generates context files without emitting or auditing the quality score."""
    proj = pathlib.Path(path).resolve()
    cfg = load_config(proj)
    analyzer = ProjectAnalyzer(
        project_path=str(proj),
        config=cfg,
        max_workers=workers,
        ignore_cache=no_cache,
        include_md=include_md,
    )
    click.echo(f"📝 Generating context for {proj.name}...")
    try:
        analyzer.analyze(output_format="markdown", generate_summary=False)
        click.secho("✅ Context generated: AI_CONTEXT.md, project_context.json", fg="green")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        sys.exit(1)


def run_audit(path: str, threshold: float):
    """Performs a security and quality audit, exits with error if below threshold."""
    proj = pathlib.Path(path).resolve()
    cfg = load_config(proj)
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    click.echo(f"🛡️  Auditing {proj.name} (Threshold: {threshold})...")
    res = analyzer.analyze()
    score = res.get("metrics", {}).get(metric_keys.QUALITY_SCORE, 0)

    if score < threshold:
        click.secho(f"❌ Audit Failed: Score {score:.1f} is below {threshold}", fg="red")
        sys.exit(1)
    else:
        click.secho(f"✅ Audit Passed: Score {score:.1f}", fg="green")
