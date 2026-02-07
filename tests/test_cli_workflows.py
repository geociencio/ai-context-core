"""Tests for CLI workflows."""

import pytest
from unittest.mock import patch
from click.testing import CliRunner
from ai_context_core.cli_groups.workflows import full_scan_cmd


@pytest.fixture
def runner():
    return CliRunner()


@patch("ai_context_core.commands.analyze.run_analysis")
@patch("ai_context_core.commands.analyze.run_audit")
@patch("ai_context_core.analyzer.gis_utils.parse_qgis_metadata")
@patch("ai_context_core.commands.qgis.check_compliance")
def test_full_scan_general_python(
    mock_qgis, mock_metadata, mock_audit, mock_analyze, runner
):
    """Test full-scan on a general Python project (no QGIS metadata)."""
    # Setup mocks
    mock_metadata.return_value = {"exists": False}

    result = runner.invoke(full_scan_cmd, ["--path", ".", "--audit-threshold", "50.0"])

    assert result.exit_code == 0
    assert "Starting Full Scan" in result.output
    # Verify sequence
    mock_analyze.assert_called_once()
    mock_audit.assert_called_once()
    mock_metadata.assert_called_once()
    # Verify logic
    mock_qgis.assert_not_called()
    assert "Skipping QGIS checks" in result.output


@patch("ai_context_core.commands.analyze.run_analysis")
@patch("ai_context_core.commands.analyze.run_audit")
@patch("ai_context_core.analyzer.gis_utils.parse_qgis_metadata")
@patch("ai_context_core.commands.qgis.check_compliance")
def test_full_scan_qgis_plugin(
    mock_qgis, mock_metadata, mock_audit, mock_analyze, runner
):
    """Test full-scan on a QGIS plugin project."""
    # Setup mocks
    mock_metadata.return_value = {"exists": True}

    result = runner.invoke(full_scan_cmd, ["--path", "."])

    assert result.exit_code == 0
    assert "QGIS Plugin detected" in result.output
    # Verify sequence
    mock_analyze.assert_called_once()
    mock_audit.assert_called_once()
    mock_qgis.assert_called_once()
