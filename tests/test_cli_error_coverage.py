import os
from click.testing import CliRunner
from unittest.mock import patch
from ai_context_core.cli import cli


def test_analyze_config_read_error():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs(
            ".ai-context/config.yaml"
        )  # Making it a dir will cause read_text error
        with open("test.py", "w") as f:
            f.write("pass")
        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0  # Should catch and pass


def test_analyze_debug_mode_error():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.analyze.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.side_effect = Exception("Debug fail")
            # Set DEBUG env var
            with patch.dict(os.environ, {"DEBUG": "1"}):
                result = runner.invoke(cli, ["analyze"])
                assert result.exit_code == 1
                assert "Error: Debug fail" in result.output
