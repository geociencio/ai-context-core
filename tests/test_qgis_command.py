import os
from click.testing import CliRunner
from ai_context_core.cli import cli


def test_qgis_command_enforces_profile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Setup mock project
        os.makedirs("mock_plugin")
        with open("mock_plugin/__init__.py", "w") as f:
            f.write(
                "class Test:\n    def __init__(self):\n        self.tr('Hello World')\n"
            )

        with open("mock_plugin/metadata.txt", "w") as f:
            f.write("[general]\nname=Mock\nqgisminimumversion=3.0\nversion=1.0\n")

        # Run qgis command
        result = runner.invoke(cli, ["qgis", "--path", "mock_plugin"])

        # Verify output
        assert result.exit_code == 0

        # Check that compliance score is NOT 0
        # If profile wasn't loaded, compliance would be disabled -> score 0
        # With profile loaded, even empty project gets some points or rules checked
        assert "QGIS Compliance Score: 0.0/100" not in result.output

        # Check specifically for i18n check output
        assert "Internationalization (i18n)" in result.output

        # Check that at least the tr() call was counted
        # The output format is "Translated strings: X/Y (Z%)"
        # We expect 1 translated string
        assert "Translated strings: 1/1" in result.output
