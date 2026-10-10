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
    source: Optional[str] = None,
):
    """Executes the full project analysis pipeline."""
    from ai_context_core.sources.base import resolve_source
    from ai_context_core.sources.pipeline import compile_context, render_context

    proj = pathlib.Path(path).resolve()
    cfg = load_config(proj)
    provider = resolve_source(
        source or "auto",
        proj,
        cfg,
        max_workers=workers,
        ignore_cache=no_cache,
        include_md=include_md,
    )

    try:
        if provider.name == "external":
            click.echo(f"🚀 Analyzing {proj.name} (source: external)...")
            result = compile_context(
                proj,
                cfg,
                "external",
                max_workers=workers,
                ignore_cache=no_cache,
                include_md=include_md,
            )
            render_context(result, proj, cfg, generate_summary=True, output_format=format)
            res = result.data
        else:
            if format != "json":
                click.echo(f"🚀 Analyzing {proj.name}...")
            analyzer = ProjectAnalyzer(
                project_path=str(proj),
                config=cfg,
                max_workers=workers,
                ignore_cache=no_cache,
                include_md=include_md,
            )
            res = analyzer.analyze(output_format=format)
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        sys.exit(1)

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


def run_context(
    path: str,
    workers: Optional[int],
    no_cache: bool,
    include_md: Optional[list] = None,
    source: Optional[str] = None,
    max_tokens: Optional[int] = None,
    check: bool = False,
):
    """Generates context files without emitting or auditing the quality score."""
    from ai_context_core.sources.pipeline import compile_context, render_context

    proj = pathlib.Path(path).resolve()
    cfg = load_config(proj)
    click.echo(f"📝 Generating context for {proj.name}...")
    try:
        result = compile_context(
            proj,
            cfg,
            source or "auto",
            max_workers=workers,
            ignore_cache=no_cache,
            include_md=include_md,
        )
        manifest = render_context(result, proj, cfg, generate_summary=False, max_tokens=max_tokens)
        total = manifest["total_tokens"]
        budget = manifest["budget"]
        if budget:
            pct = int(round(total * 100 / budget))
            click.echo(f"   context: {total:,} / {budget:,} tokens ({pct}%)")
        else:
            click.echo(f"   context: {total:,} tokens")
        click.secho(
            f"✅ Context generated ({result.provenance.source}): "
            "AI_CONTEXT.md, project_context.json, context_manifest.json",
            fg="green",
        )
        if check:
            from ai_context_core.context.verify import verify_context

            report = verify_context(proj)
            if not report["fresh"]:
                click.secho(f"Context check failed: {report['reason']}", fg="red", err=True)
                sys.exit(1)
            click.echo("Context check: fresh.")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        sys.exit(1)
