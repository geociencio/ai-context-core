"""Tests for token budgeting and the context manifest (F3)."""

import json
import pathlib

from click.testing import CliRunner

from ai_context_core.cli import cli
from ai_context_core.context.budget import (
    TokenBudget,
    apply_budget,
    budget_from_config,
    estimate_tokens,
    truncate_lines,
)
from ai_context_core.context.manifest import measure_manifest, render_sections


def _sections():
    return [
        ("structure", ["## STRUCTURE", "s" * 80, "s" * 80, "s" * 80]),
        ("metrics", ["## METRICS", "m" * 80, "m" * 80]),
        ("git", ["## GIT", "g" * 80]),
    ]


# --- estimation --------------------------------------------------------------


def test_estimate_tokens_heuristic():
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2
    assert estimate_tokens("a" * 400) == 100


# --- truncation --------------------------------------------------------------


def test_truncate_lines_no_limit():
    lines, tokens, truncated = truncate_lines(["a", "b"], None)
    assert truncated is False
    assert tokens == estimate_tokens("a\nb")


def test_truncate_lines_inserts_marker_and_is_exact():
    lines = ["x" * 40, "y" * 40, "z" * 40]
    kept, tokens, truncated = truncate_lines(lines, 12)
    assert truncated is True
    assert kept[0] == lines[0]
    assert kept[-1].startswith("... [truncated:")
    assert tokens == estimate_tokens("\n".join(kept))


# --- budget resolution -------------------------------------------------------


def test_budget_from_config_cli_override():
    config = {"context": {"budget": {"max_tokens": 5000, "sections": {"git": 100}}}}
    b = budget_from_config(config, max_tokens=1000)
    assert b.max_tokens == 1000
    assert b.per_section == {"git": 100}
    assert b.enabled


def test_budget_from_config_empty_is_disabled():
    assert budget_from_config({}).enabled is False


# --- apply_budget ------------------------------------------------------------


def test_apply_budget_global_drops_trailing_sections():
    budget = TokenBudget(max_tokens=60)
    counted, total, truncated = apply_budget(_sections(), budget)
    assert truncated is True
    assert total <= budget.max_tokens
    assert counted[0][0] == "structure"
    assert len(counted) < len(_sections())


def test_apply_budget_per_section_limit():
    budget = TokenBudget(per_section={"structure": 60})
    counted, _total, truncated = apply_budget(_sections(), budget)
    names = {name: tokens for name, _lines, tokens in counted}
    assert truncated is True
    assert names["structure"] <= 60


# --- render + manifest -------------------------------------------------------


def test_render_sections_manifest_is_consistent():
    header = ["# TITLE", "gen", ""]
    lines, manifest = render_sections(header, _sections(), TokenBudget())
    content = "\n".join(lines)

    assert manifest["total_tokens"] == estimate_tokens(content)
    assert (
        manifest["header_tokens"] + sum(manifest["sections"].values()) == manifest["total_tokens"]
    )
    assert set(manifest["sections"]) == {"structure", "metrics", "git"}


def test_render_sections_respects_hard_cap():
    header = ["# TITLE", "gen", ""]
    lines, manifest = render_sections(header, _sections(), TokenBudget(max_tokens=60))
    content = "\n".join(lines)
    assert estimate_tokens(content) <= 60
    assert manifest["truncated"] is True


def test_measure_manifest_matches_sections():
    header = ["# T", ""]
    sections = [("a", ["1", "2"]), ("b", ["3"])]
    manifest = measure_manifest(header, sections, False, None)
    assert manifest["total_tokens"] == estimate_tokens("\n".join(header + ["1", "2", "3"]))
    assert (
        manifest["header_tokens"] + sum(manifest["sections"].values()) == manifest["total_tokens"]
    )


# --- CLI ---------------------------------------------------------------------


def _project() -> None:
    pkg = pathlib.Path("pkg")
    pkg.mkdir(exist_ok=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "cli.py").write_text(
        "def main():\n    if True:\n        return 1\n\nif __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )


def test_context_cli_writes_manifest_and_respects_budget():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _project()
        result = runner.invoke(
            cli, ["context", "--no-cache", "--source", "builtin", "--max-tokens", "60"]
        )
        assert result.exit_code == 0, result.output
        assert "tokens" in result.output
        assert pathlib.Path("context_manifest.json").exists()

        content = pathlib.Path("AI_CONTEXT.md").read_text(encoding="utf-8")
        manifest = json.loads(pathlib.Path("context_manifest.json").read_text(encoding="utf-8"))
        assert manifest["total_tokens"] == estimate_tokens(content)
        assert manifest["total_tokens"] <= 60
        assert manifest["budget"] == 60


def test_context_cli_is_deterministic():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _project()
        runner.invoke(cli, ["context", "--no-cache", "--source", "builtin", "--max-tokens", "60"])
        first = pathlib.Path("AI_CONTEXT.md").read_text(encoding="utf-8")
        # Remove generated artifacts so the structure tree matches the first run
        # (otherwise AI_CONTEXT.md itself becomes part of the analyzed tree).
        for name in (
            "AI_CONTEXT.md",
            "project_context.json",
            "context_manifest.json",
            ".ai_context_cache.json",
        ):
            pathlib.Path(name).unlink(missing_ok=True)
        runner.invoke(cli, ["context", "--no-cache", "--source", "builtin", "--max-tokens", "60"])
        second = pathlib.Path("AI_CONTEXT.md").read_text(encoding="utf-8")
        assert first == second
