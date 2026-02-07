"""QGIS compliance command logic."""

import pathlib
import click
from ..analyzer.engine import ProjectAnalyzer
from ..config.loader import ConfigLoader


def validate_qgis(path: str):
    """Validates QGIS plugin compliance."""
    proj = pathlib.Path(path).resolve()
    loader = ConfigLoader()
    # For QGIS validation, we explicitly use the qgis profile to ensure qgis compliance is enabled
    cfg = loader.load_config(profile_name="qgis")
    analyzer = ProjectAnalyzer(project_path=str(proj), config=cfg)
    res = analyzer.analyze()

    qgis = res.get("qgis_compliance", {})
    metadata = qgis.get("metadata", {})

    click.secho("🗺️  QGIS PLUGIN VALIDATION", fg="green", bold=True)

    _show_metadata_validation(metadata)
    _show_i18n_stats(qgis)
    _show_qt_transition(qgis)

    score = qgis.get("compliance_score", 0)
    click.secho(
        f"\n🏆 QGIS Compliance Score: {score:.1f}/100",
        fg="green" if score > 70 else "yellow",
    )


def _show_metadata_validation(metadata):
    if metadata.get("valid"):
        click.secho("\n✅ metadata.txt is valid", fg="green")
        content = metadata.get("content", {})
        click.echo(f"Plugin Name: {content.get('name', 'N/A')}")
        click.echo(f"Version: {content.get('version', 'N/A')}")
        click.echo(f"QGIS Min Version: {content.get('qgisminimumversion', 'N/A')}")
    else:
        click.secho("\n❌ metadata.txt validation failed", fg="red")
        for err in metadata.get("errors", []):
            click.echo(f"  - {err}")


def _show_i18n_stats(qgis):
    i18n = qgis.get("i18n_stats", {})
    total_tr = i18n.get("total_tr", 0)
    total_strings = i18n.get("total_strings", 0)
    coverage = (total_tr / total_strings * 100) if total_strings > 0 else 0
    click.secho("\n🌍 Internationalization (i18n)", fg="cyan", bold=True)
    click.echo(f"Translated strings: {total_tr}/{total_strings} ({coverage:.1f}%)")


def _show_qt_transition(qgis):
    qt = qgis.get("qt_transition", {})
    pyqt5_count = qt.get("pyqt5_count", 0)
    pyqt6_count = qt.get("pyqt6_count", 0)
    click.secho("\n🔄 Qt6 Transition Readiness", fg="yellow", bold=True)
    if pyqt5_count == 0:
        click.secho("✅ No PyQt5 imports detected (Qt6 ready!)", fg="green")
    else:
        click.secho(f"⚠️  {pyqt5_count} PyQt5 imports found", fg="yellow")
    if pyqt6_count > 0:
        click.echo(f"PyQt6 imports: {pyqt6_count}")
