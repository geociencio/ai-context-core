"""Regression tests for render fingerprints and extended staleness detection."""

import json
import pathlib

from ai_context_core.analyzer.providers.config_loader import load_config
from ai_context_core.context.symbol_index import build_symbol_index, write_symbol_index
from ai_context_core.context.verify import verify_context
from ai_context_core.sources.pipeline import compile_context, render_context


def _write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _project(root: pathlib.Path) -> None:
    _write(root / "pkg" / "__init__.py", "")
    _write(root / "pkg" / "mod.py", "def f():\n    return 1\n")


def _render(root: pathlib.Path) -> dict:
    config = load_config(root)
    result = compile_context(root, config, "builtin", ignore_cache=True)
    render_context(result, root, config)
    return config


def _config_file(root: pathlib.Path, content: str) -> None:
    _write(root / ".ai-context" / "config.toml", content)


def test_render_records_fingerprint_and_config_hash(tmp_path):
    _project(tmp_path)
    config = _render(tmp_path)

    manifest = json.loads((tmp_path / "context_manifest.json").read_text())
    project = json.loads((tmp_path / "project_context.json").read_text())

    assert manifest["_meta"]["render_fingerprint"].startswith("sha256:")
    assert manifest["_meta"]["config_hash"]
    assert project["_meta"]["render_fingerprint"] == manifest["_meta"]["render_fingerprint"]
    assert config["context"]["budget"]["max_tokens"] == 8000


def test_verify_detects_configuration_change(tmp_path):
    _project(tmp_path)
    _config_file(tmp_path, "[context]\nmermaid_style = false\n")
    _render(tmp_path)
    assert verify_context(tmp_path)["fresh"] is True

    _config_file(tmp_path, "[context]\nmermaid_style = true\n")
    report = verify_context(tmp_path)

    assert report["fresh"] is False
    assert "configuration changed" in report["reason"]


def test_verify_detects_embedded_document_change(tmp_path):
    _project(tmp_path)
    _config_file(tmp_path, 'context_docs = ["ARCHITECTURE.md"]\n')
    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n\nOriginal.\n")
    _render(tmp_path)
    assert verify_context(tmp_path)["fresh"] is True

    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n\nEdited.\n")
    report = verify_context(tmp_path)

    assert report["fresh"] is False
    assert "embedded context docs" in report["reason"]


def test_verify_detects_stale_and_missing_symbols(tmp_path):
    _project(tmp_path)
    write_symbol_index(tmp_path, build_symbol_index(tmp_path))
    _render(tmp_path)
    assert verify_context(tmp_path)["fresh"] is True

    symbols_path = tmp_path / "symbols.json"
    symbols = json.loads(symbols_path.read_text())
    symbols["_meta"]["content_hash"] = "sha256:stale"
    symbols_path.write_text(json.dumps(symbols), encoding="utf-8")

    report = verify_context(tmp_path)
    assert report["fresh"] is False
    assert report["symbols"]["fresh"] is False
    assert "stale" in report["reason"]

    symbols_path.unlink()
    report = verify_context(tmp_path)
    assert report["fresh"] is False
    assert "symbols.json" in report["missing"]


def test_verify_legacy_artifacts_fall_back_to_content_hash(tmp_path):
    _project(tmp_path)
    _render(tmp_path)

    manifest_path = tmp_path / "context_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["_meta"].pop("render_fingerprint", None)
    manifest["_meta"].pop("config_hash", None)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    report = verify_context(tmp_path)

    assert report["fresh"] is True
    assert report["legacy"] is True
