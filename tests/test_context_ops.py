"""Tests for verify / symbols / health (F4)."""

import json
import pathlib

from click.testing import CliRunner

from ai_context_core.cli import cli
from ai_context_core.context.health import compute_health
from ai_context_core.context.symbol_index import (
    build_symbol_index,
    search_symbols,
    write_symbol_index,
)
from ai_context_core.context.verify import compute_content_hash, verify_context
from ai_context_core.sources.pipeline import compile_context, render_context


def _write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _project(root: pathlib.Path) -> None:
    _write(root / "pkg" / "__init__.py", "")
    _write(
        root / "pkg" / "cli.py",
        "def main():\n    helper()\n\n\nclass App:\n    def run(self):\n        return helper()\n\n"
        "def helper():\n    return 1\n\n\nif __name__ == '__main__':\n    main()\n",
    )


def _render(root: pathlib.Path) -> None:
    result = compile_context(root, {}, "builtin")
    render_context(result, root, {})


# --- content hash ------------------------------------------------------------


def test_content_hash_stable_and_sensitive(tmp_path):
    _project(tmp_path)
    first = compute_content_hash(tmp_path)
    assert first == compute_content_hash(tmp_path)
    assert first.startswith("sha256:")

    _write(tmp_path / "pkg" / "cli.py", "def main():\n    return 0\n")
    assert compute_content_hash(tmp_path) != first


# --- verify ------------------------------------------------------------------


def test_verify_missing_hash(tmp_path):
    _project(tmp_path)
    report = verify_context(tmp_path)
    assert report["fresh"] is False
    assert "no recorded content hash" in report["reason"]


def test_verify_fresh_then_stale(tmp_path):
    _project(tmp_path)
    _render(tmp_path)
    assert verify_context(tmp_path)["fresh"] is True

    _write(tmp_path / "pkg" / "cli.py", "def main():\n    return 42\n")
    report = verify_context(tmp_path)
    assert report["fresh"] is False
    assert "changed" in report["reason"]


def test_verify_missing_artifact(tmp_path):
    _project(tmp_path)
    _render(tmp_path)
    (tmp_path / "context_manifest.json").unlink()
    (tmp_path / "project_context.json").unlink()
    report = verify_context(tmp_path)
    assert report["fresh"] is False
    assert "context_manifest.json" in report["missing"]


# --- symbol index ------------------------------------------------------------


def test_build_symbol_index_definitions_and_references(tmp_path):
    _project(tmp_path)
    index = build_symbol_index(tmp_path)

    by_kind = {}
    for sym in index["symbols"]:
        by_kind.setdefault(sym["kind"], []).append(sym["name"])
    assert "module" in by_kind
    assert "main" in by_kind["function"]
    assert "helper" in by_kind["function"]
    assert "App" in by_kind["class"]
    assert "run" in by_kind["method"]

    refs = {r["name"] for r in index["references"]}
    assert "helper" in refs and "main" in refs


def test_search_symbols_returns_file_line(tmp_path):
    _project(tmp_path)
    index = build_symbol_index(tmp_path)
    matches = search_symbols(index, "helper")
    assert any(m.startswith("pkg/cli.py:") and "helper" in m for m in matches)


def test_write_and_load_symbol_index(tmp_path):
    _project(tmp_path)
    index = build_symbol_index(tmp_path)
    write_symbol_index(tmp_path, index)
    assert json.loads((tmp_path / "symbols.json").read_text())["schema"] == 1


# --- health ------------------------------------------------------------------


def test_compute_health_reports_all_sections(tmp_path):
    _project(tmp_path)
    _render(tmp_path)
    write_symbol_index(tmp_path, build_symbol_index(tmp_path))

    report = compute_health(tmp_path)
    assert report["fresh"] is True
    assert report["tokens"]["total"] is not None
    assert report["symbols"]["definitions"] > 0
    assert report["provenance"]["source"] == "builtin"


# --- CLI ---------------------------------------------------------------------


def test_cli_verify_exit_codes():
    runner = CliRunner()
    with runner.isolated_filesystem():
        root = pathlib.Path(".")
        _project(root)
        runner.invoke(cli, ["context", "--no-cache", "--source", "builtin"])
        assert runner.invoke(cli, ["verify"]).exit_code == 0

        _write(root / "pkg" / "cli.py", "def main():\n    return 9\n")
        assert runner.invoke(cli, ["verify"]).exit_code == 1


def test_cli_context_check_gate():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _project(pathlib.Path("."))
        result = runner.invoke(cli, ["context", "--no-cache", "--source", "builtin", "--check"])
        assert result.exit_code == 0
        assert "fresh" in result.output.lower()


def test_cli_symbols_grep():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _project(pathlib.Path("."))
        result = runner.invoke(cli, ["symbols", "--grep", "helper"])
        assert result.exit_code == 0
        assert "pkg/cli.py:" in result.output


def test_cli_health_stale_exit_1():
    runner = CliRunner()
    with runner.isolated_filesystem():
        _project(pathlib.Path("."))
        result = runner.invoke(cli, ["health"])
        assert result.exit_code == 1
        assert "CONTEXT HEALTH" in result.output
