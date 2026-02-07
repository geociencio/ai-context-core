from ai_context_core.commands.report import (
    _show_patterns,
    _show_security,
    _show_recommendations,
)
from unittest.mock import patch


def test_report_show_patterns_empty():
    # Coverage for report.py line 29
    with patch("click.echo") as mock_echo:
        _show_patterns({"patterns": {}})
        # Should print "No patterns detected."
        mock_echo.assert_called_with("No patterns detected.")


def test_report_show_security_empty():
    # Coverage for report.py line 42
    with patch("click.echo") as mock_echo:
        _show_security({"security": []})
        # Should print "No issues found."
        mock_echo.assert_called_with("No issues found.")


def test_report_show_recommendations_empty():
    # Coverage for report.py line 55
    with patch("click.echo") as mock_echo:
        _show_recommendations({"optimizations": []})
        # Should print "No recommendations."
        mock_echo.assert_called_with("No recommendations.")
