import os
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ai_context_core.cli import cli


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


def test_analyze_command_full():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("def foo():\n    # TODO: fix it\n    pass")

        result = runner.invoke(cli, ["analyze", "--no-cache"])
        assert result.exit_code == 0
        assert "ai-ctx Quality Score" in result.output
        assert "Completed" in result.output


def test_context_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("def foo():\n    pass")

        result = runner.invoke(cli, ["context", "--no-cache"])
        assert result.exit_code == 0
        assert "Context generated" in result.output
        assert "ai-ctx Quality Score" not in result.output
        assert os.path.exists("AI_CONTEXT.md")
        assert os.path.exists("project_context.json")
        assert not os.path.exists("PROJECT_SUMMARY.md")


def test_git_command_success():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch(
            "ai_context_core.cli.commands.git.git_analysis.GitAnalyzer"
        ) as mock_analyzer_cls:
            mock_analyzer = MagicMock()
            mock_analyzer_cls.return_value = mock_analyzer
            mock_analyzer.is_repo.return_value = True
            mock_analyzer.get_hotspots.return_value = [{"path": "file1.py", "commits": 10}]
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


def test_analyze_local_config():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs(".ai-context")
        with open(".ai-context/config.toml", "w") as f:
            f.write('profile_name = "generic"\n[quality_thresholds]\nscore = 90')

        with open("test.py", "w") as f:
            f.write("def foo(): pass")

        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0
        assert "🚀 Analyzing" in result.output


def test_analyze_error_handling():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch("ai_context_core.sources.pipeline.compile_context") as mock_analyze:
            mock_analyze.side_effect = Exception("Analysis failed")
            result = runner.invoke(cli, ["analyze"])
            assert result.exit_code == 1
            assert "Error: Analysis failed" in result.output


def test_deps_command_extended():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch("ai_context_core.cli.commands.deps.ProjectAnalyzer.collect") as mock_analyze:
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


def test_deps_command_no_findings():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch("ai_context_core.cli.commands.deps.ProjectAnalyzer.collect") as mock_analyze:
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
            "ai_context_core.cli.commands.git.git_analysis.GitAnalyzer"
        ) as mock_analyzer_cls:
            mock_analyzer = MagicMock()
            mock_analyzer_cls.return_value = mock_analyzer
            mock_analyzer.is_repo.return_value = True
            mock_analyzer.get_hotspots.return_value = []
            mock_analyzer.get_churn.return_value = {"available": False}

            result = runner.invoke(cli, ["git"])
            assert "No hotspots found" in result.output
            assert "No churn data available" in result.output
