"""Analysis and audit command logic."""

import pathlib
import os
import sys
import click
from typing import Optional
from ..analyzer.engine import ProjectAnalyzer
from ..config.loader import ConfigLoader


def run_analysis(path: str, workers: Optional[int], format: str, no_cache: bool):
    """Executes the full project analysis pipeline."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    local_cfg_path = proj / ".ai-context" / "config.yaml"
    local_cfg = {}
    if local_cfg_path.exists():
        try:
            import yaml

            local_cfg = yaml.safe_load(local_cfg_path.read_text()) or {}
        except Exception:
            pass

    cfg = loader.load_config(
        profile_name=local_cfg.get("profile_name"), override_config=local_cfg
    )
    analyzer = ProjectAnalyzer(
        project_path=str(proj),
        config=cfg,
        max_workers=workers,
        ignore_cache=no_cache,
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
        q = m.get("quality_score", 0)
        click.echo("-" * 40)
        click.secho(
            f"🏆 Quality Score: {q:.1f}/100", fg="green" if q > 80 else "yellow"
        )
        click.echo(
            f"📊 Lines: {m.get('total_lines_code', 0):,}\n💡 Opts: {len(res.get('optimizations', []))}"
        )
        click.echo("-" * 40)
        click.secho("✅ Completed.", fg="green")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        if os.environ.get("DEBUG"):
            raise e
        sys.exit(1)


def run_audit(path: str, threshold: float):
    """Performs a security and quality audit, exits with error if below threshold."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    cfg = loader.load_config()
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    click.echo(f"🛡️  Auditing {proj.name} (Threshold: {threshold})...")
    res = analyzer.analyze()
    score = res.get("metrics", {}).get("quality_score", 0)

    if score < threshold:
        click.secho(
            f"❌ Audit Failed: Score {score:.1f} is below {threshold}", fg="red"
        )
        sys.exit(1)
    else:
        click.secho(f"✅ Audit Passed: Score {score:.1f}", fg="green")
