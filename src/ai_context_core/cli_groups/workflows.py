"""Compound workflow commands for ai-context-core."""

import click
import sys
from pathlib import Path
from ai_context_core.commands import analyze, qgis
from ai_context_core.analyzer import gis_utils


@click.command(name="full-scan")
@click.option("--path", default=".", help="Project path to scan")
@click.option("--audit-threshold", default=80.0, help="Minimum Quality Score for audit")
@click.option("--format", default="markdown", type=click.Choice(["markdown", "html"]))
def full_scan_cmd(path: str, audit_threshold: float, format: str):
    """Run a complete project scan (Analyze -> Audit -> QGIS Check).

    Automatically detects if the project is a QGIS plugin.
    """
    project_path = Path(path).resolve()
    click.echo(f"🚀 Starting Full Scan for: {project_path}")

    # 1. Main Analysis
    click.echo("\n🔍 [1/3] Running Static Analysis...")
    try:
        analyze.run_analysis(
            str(project_path), workers=None, format=format, no_cache=False
        )
        click.echo("✅ Analysis complete.")
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}", err=True)
        sys.exit(1)

    # 2. Quality Audit
    click.echo(f"\n🛡️ [2/3] Verifying Quality Score (Threshold: {audit_threshold})...")
    try:
        analyze.run_audit(str(project_path), threshold=audit_threshold)
        click.echo("✅ Audit passed.")
    except SystemExit as e:
        if e.code != 0:
            click.echo("❌ Audit failed (Score too low).", err=True)
            # We don't exit here to allow seeing QGIS results, unless strict mode is desired
            # letting it continue for now to be "report-like"
        else:
            click.echo("✅ Audit passed.")
    except Exception as e:
        click.echo(f"❌ Audit error: {e}", err=True)

    # 3. Auto-detection & QGIS Check
    click.echo("\n🌍 [3/3] Checking Project Type...")

    # Check for metadata.txt
    metadata_res = gis_utils.parse_qgis_metadata(project_path)
    is_qgis = metadata_res["exists"]

    if is_qgis:
        click.echo("✅ QGIS Plugin detected (metadata.txt found).")
        click.echo("   Running compliance checks...")
        try:
            # qgis module needs to expose a function that doesn't just print but returns or raises
            # Assuming check_compliance handles printing
            # We reuse the threshold from audit or a default
            qgis.check_compliance(str(project_path), threshold=70.0)
        except Exception as e:
            click.echo(f"❌ QGIS Check error: {e}", err=True)
    else:
        click.echo("ℹ️ QGIS metadata.txt not found.")
        click.echo("   Skipping QGIS checks (General Python project detected).")

    click.echo("\n🏁 Full Scan Completed.")
