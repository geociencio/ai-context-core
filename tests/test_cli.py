import os
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ai_context_core.cli import cli


def test_init_command_with_qgis_profile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init", "--profile", "qgis"])
        assert result.exit_code == 0
        assert os.path.exists(".ai-context/config.toml")


def test_init_command_with_generic_profile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert not os.path.exists(".ai-context/config.toml")
        assert not os.path.exists(".ai-context/config.yaml")


def test_analyze_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a dummy file to analyze
        with open("test.py", "w") as f:
            f.write("def hello():\n")
            f.write("    print('hello')\n")

        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0


def test_profiles_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["profiles"])
    assert result.exit_code == 0
    assert "generic" in result.output
    assert "qgis" in result.output


def test_specialized_report_commands():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Initialize
        runner.invoke(cli, ["init"])

        # Create a dummy file with findings
        with open("my_code.py", "w") as f:
            f.write(
                """
class MySingleton:
    _instance = None
    @classmethod
    def get_instance(cls): return cls._instance

import os
def insecure():
    os.system("ls") # Security issue

def complex_one(a):
    if a > 1:
        if a > 1:
            if a > 1:
                if a > 1:
                    if a > 1:
                        if a > 1:
                            if a > 1:
                                if a > 1:
                                    if a > 1:
                                        if a > 1:
                                            if a > 1:
                                                if a > 1:
                                                    if a > 1:
                                                        if a > 1:
                                                            if a > 1:
                                                                if a > 1:
                                                                    return a
def f1(): pass
def f2(): pass
def f3(): pass
def f4(): pass
def f5(): pass
def f6(): pass
"""
            )

        # Test patterns
        result = runner.invoke(cli, ["patterns"])
        print(f"PATTERNS OUTPUT: {result.output}")
        assert result.exit_code == 0
        assert "Singleton" in result.output

        # Test security
        result = runner.invoke(cli, ["security"])
        assert result.exit_code == 0
        assert "SECURITY ISSUES" in result.output

        # Test help-me
        result = runner.invoke(cli, ["help-me"])
        assert result.exit_code == 0
        assert "AI RECOMMENDATIONS" in result.output


def test_clean_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create some artifacts
        artifacts = [
            ".ai_context_cache.json",
            "AI_CONTEXT.md",
            "ANALYSIS_REPORT.md",
        ]
        for a in artifacts:
            with open(a, "w") as f:
                f.write("test")

        # Test dry-run
        result = runner.invoke(cli, ["clean", "--dry-run"])
        assert result.exit_code == 0
        assert "Would delete: .ai_context_cache.json" in result.output
        for a in artifacts:
            assert os.path.exists(a)

        # Test actual clean
        result = runner.invoke(cli, ["clean"])
        assert result.exit_code == 0
        assert "Cleaned 3 file(s)" in result.output
        for a in artifacts:
            assert not os.path.exists(a)


def test_stats_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a dummy file
        with open("test.py", "w") as f:
            f.write("def foo():\n    pass\n")

        result = runner.invoke(cli, ["stats"])
        assert result.exit_code == 0
        assert "PROJECT STATISTICS" in result.output
        assert "Source Lines (SLOC)" in result.output


def test_deps_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("a.py", "w") as f:
            f.write("import b")
        with open("b.py", "w") as f:
            f.write("import a")

        # Test with cycles and metrics
        result = runner.invoke(cli, ["deps", "--cycles", "--metrics"])
        assert result.exit_code == 0
        assert "CIRCULAR DEPENDENCIES" in result.output
        assert "DEPENDENCY METRICS" in result.output


def test_git_command_no_repo():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Running in a non-git repo should fail
        result = runner.invoke(cli, ["git"])
        assert result.exit_code != 0
        assert "Not a git repository" in result.output


def test_audit_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("def foo(): pass")

        # Audit passing
        result = runner.invoke(cli, ["audit", "--threshold", "0"])
        assert result.exit_code == 0
        assert "Audit Passed" in result.output

        # Audit failing (should exit with 1)
        result = runner.invoke(cli, ["audit", "--threshold", "101"])
        assert result.exit_code == 1
        assert "Audit Failed" in result.output


def test_analyze_command_full():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("def foo():\n    # TODO: fix it\n    pass")

        result = runner.invoke(cli, ["analyze", "--no-cache"])
        assert result.exit_code == 0
        assert "Quality Score" in result.output
        assert "Completed" in result.output


def test_inspect_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("def foo():\n    pass")

        result = runner.invoke(cli, ["inspect", "test.py"])
        assert result.exit_code == 0
        assert "Inspecting test.py" in result.output
        assert "Module: test.py" in result.output

        # Test non-existent file
        result = runner.invoke(cli, ["inspect", "missing.py"])
        assert result.exit_code == 1
        assert "File not found" in result.output

        # Test syntax error (unbalanced parens)
        with open("error.py", "w") as f:
            f.write("def foo(")
        result = runner.invoke(cli, ["inspect", "error.py"])
        assert result.exit_code == 1
        assert "Syntax Error" in result.output


def test_git_command_success():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.git.git_analysis.GitAnalyzer"
        ) as mock_analyzer_cls:
            mock_analyzer = MagicMock()
            mock_analyzer_cls.return_value = mock_analyzer
            mock_analyzer.is_repo.return_value = True
            mock_analyzer.get_hotspots.return_value = [
                {"path": "file1.py", "commits": 10}
            ]
            mock_analyzer.get_churn.return_value = {
                "available": True,
                "files_changed": 5,
                "added": 100,
                "deleted": 50,
                "total_churn": 150,
            }

            result = runner.invoke(cli, ["git"])
            assert result.exit_code == 0
            assert "GIT HOTSPOTS" in result.output
            assert "file1.py" in result.output
            assert "CODE CHURN" in result.output
            assert "Total Churn: 150" in result.output


def test_serve_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with (
            patch(
                "ai_context_core.commands.serve.socketserver.TCPServer"
            ) as mock_server_cls,
            patch("ai_context_core.commands.serve.webbrowser.open") as mock_open,
        ):
            # Setup mock server that stops immediately
            mock_server = MagicMock()
            mock_server_cls.return_value.__enter__.return_value = mock_server
            mock_server.serve_forever.side_effect = KeyboardInterrupt()

            result = runner.invoke(cli, ["serve", "--port", "8000"])
            assert "Serving report at: http://localhost:8000" in result.output
            assert "Server stopped" in result.output

            # Test with browser open
            mock_server.serve_forever.side_effect = KeyboardInterrupt()
            result = runner.invoke(cli, ["serve", "--open"])
            mock_open.assert_called()


def test_serve_command_error():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.serve.socketserver.TCPServer"
        ) as mock_server_cls:
            mock_server_cls.side_effect = Exception("Port in use")
            result = runner.invoke(cli, ["serve"])
            assert "Server error: Port in use" in result.output


def test_analyze_local_config():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs(".ai-context")
        with open(".ai-context/config.toml", "w") as f:
            f.write("profile_name = \"generic\"\n[quality_thresholds]\nscore = 90")

        with open("test.py", "w") as f:
            f.write("def foo(): pass")

        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0
        assert "🚀 Analyzing" in result.output


def test_analyze_error_handling():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.analyze.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.side_effect = Exception("Analysis failed")
            result = runner.invoke(cli, ["analyze"])
            assert result.exit_code == 1
            assert "Error: Analysis failed" in result.output


def test_deps_command_extended():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.deps.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.return_value = {
                "dependencies": {
                    "unused_imports": {"mod1.py": ["os", "sys"]},
                    "circular_dependencies": [["a", "b", "a"]],
                    "graph_metrics": {
                        "nodes": 10,
                        "edges": 20,
                        "density": 0.5,
                        "is_dag": False,
                    },
                    "coupling_metrics": {"mod1.py": {"cbo": 5}},
                }
            }
            result = runner.invoke(cli, ["deps", "--unused", "--cycles", "--metrics"])
            assert result.exit_code == 0
            assert "UNUSED IMPORTS" in result.output
            assert "mod1.py" in result.output
            assert "CIRCULAR DEPENDENCIES" in result.output
            assert "a → b → a" in result.output
            assert "DEPENDENCY METRICS" in result.output
            assert "CBO=5" in result.output


def test_qgis_command_extended():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.qgis.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.return_value = {
                "qgis_compliance": {
                    "metadata": {"valid": False, "errors": ["Missing field: about"]},
                    "i18n_stats": {"total_tr": 5, "total_strings": 10},
                    "qt_transition": {"pyqt5_count": 2, "pyqt6_count": 1},
                    "compliance_score": 50.0,
                }
            }
            result = runner.invoke(cli, ["qgis"])
            assert result.exit_code == 0
            assert "metadata.txt validation failed" in result.output
            assert "Missing field: about" in result.output
            assert "Translated strings: 5/10 (50.0%)" in result.output
            assert "2 PyQt5 imports found" in result.output
            assert "PyQt6 imports: 1" in result.output


def test_deps_command_no_findings():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.deps.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.return_value = {
                "dependencies": {
                    "unused_imports": {},
                    "circular_dependencies": [],
                    "graph_metrics": {},
                    "coupling_metrics": {},
                }
            }
            result = runner.invoke(cli, ["deps", "--unused", "--cycles", "--metrics"])
            assert "No unused imports detected" in result.output
            assert "No circular dependencies detected" in result.output


def test_git_command_no_findings():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.git.git_analysis.GitAnalyzer"
        ) as mock_analyzer_cls:
            mock_analyzer = MagicMock()
            mock_analyzer_cls.return_value = mock_analyzer
            mock_analyzer.is_repo.return_value = True
            mock_analyzer.get_hotspots.return_value = []
            mock_analyzer.get_churn.return_value = {"available": False}

            result = runner.invoke(cli, ["git"])
            assert "No hotspots found" in result.output
            assert "No churn data available" in result.output


def test_qgis_command_metadata_valid_content():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.commands.qgis.ProjectAnalyzer.analyze"
        ) as mock_analyze:
            mock_analyze.return_value = {
                "qgis_compliance": {
                    "metadata": {
                        "valid": True,
                        "content": {
                            "name": "TestPlugin",
                            "version": "1.0",
                            "qgisminimumversion": "3.0",
                        },
                    },
                    "compliance_score": 100,
                }
            }
            result = runner.invoke(cli, ["qgis"])
            assert "metadata.txt is valid" in result.output
            assert "Plugin Name: TestPlugin" in result.output
