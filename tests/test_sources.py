"""Tests for the pluggable analysis source layer (F1)."""

import json
import pathlib

import pytest
from click.testing import CliRunner

from ai_context_core.cli import cli
from ai_context_core.model import AnalysisResult, Provenance
from ai_context_core.sources.base import (
    VALID_SOURCES,
    external_output_path,
    requested_source,
    resolve_source,
)
from ai_context_core.sources.builtin.engine_source import BuiltinSource
from ai_context_core.sources.external.qgis_analyzer import ExternalSource, map_project_context
from ai_context_core.sources.pipeline import compile_context


def _external_payload() -> dict:
    """Return a minimal but realistic qgis-analyzer payload (schema v1)."""
    return {
        "schema_version": 1,
        "analyzer_version": "1.14.0",
        "project_name": "demo",
        "metrics": {
            "total_files": 2,
            "total_lines": 40,
            "quality_score": 72.5,
            "maintainability_score": 88.0,
        },
        "modules": [
            {
                "path": "pkg/__init__.py",
                "lines": 10,
                "complexity": 1,
                "functions": [{"name": "a"}],
                "classes": [],
                "imports": ["os"],
                "has_main": False,
                "docstrings": {"coverage": 1.0},
                "syntax_error": False,
            },
            {
                "path": "pkg/cli.py",
                "lines": 30,
                "complexity": 5,
                "functions": [{"name": "main"}, {"name": "run"}],
                "classes": [{"name": "App"}],
                "imports": ["sys", "pkg"],
                "has_main": True,
                "docstrings": {"coverage": 0.5},
                "syntax_error": False,
            },
        ],
        "semantic": {
            "circular_dependencies": [["a", "b"]],
            "coupling_metrics": {"pkg/cli.py": {"fan_in": 2, "fan_out": 3}},
        },
        "qgis_compliance": {"compliance_score": 90},
        "security": {"findings": [], "count": 0},
    }


def _write_external(root: pathlib.Path, payload: dict) -> pathlib.Path:
    out_dir = root / "analysis_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "project_context.json"
    target.write_text(json.dumps(payload), encoding="utf-8")
    return target


# --- model -------------------------------------------------------------------


def test_analysis_result_with_meta():
    result = AnalysisResult(
        data={"project_name": "x"},
        provenance=Provenance(source="external", schema=1, tool_version="1.2.3", git_sha="abc"),
    )
    meta = result.with_meta()
    assert meta["project_name"] == "x"
    assert meta["_meta"]["source"] == "external"
    assert meta["_meta"]["schema"] == 1
    assert meta["_meta"]["tool_version"] == "1.2.3"
    assert meta["_meta"]["git_sha"] == "abc"


# --- external mapping --------------------------------------------------------


def test_map_project_context_metrics_and_modules():
    data = map_project_context(_external_payload(), fallback_name="fallback")

    assert data["project_name"] == "demo"
    assert data["metrics"]["quality_score"] == 72.5
    assert data["metrics"]["total_functions"] == 3
    assert data["metrics"]["total_classes"] == 1
    assert data["metrics"]["max_complexity"] == 5
    assert data["complexity"]["total_modules"] == 2
    assert len(data["modules"]) == 2
    assert data["entry_points"] == [{"path": "pkg/cli.py", "type": "unknown"}]
    assert data["dependencies"]["circular_dependencies"] == [["a", "b"]]
    assert data["dependencies"]["coupling_metrics"]["pkg/cli.py"]["cbo"] == 5
    # Context-owned sections are intentionally absent (filled by the pipeline).
    assert "structure" not in data
    assert "git" not in data
    assert "manual_notes" not in data


def test_map_project_context_fallback_name():
    payload = _external_payload()
    payload.pop("project_name")
    assert map_project_context(payload, fallback_name="fallback")["project_name"] == "fallback"


# --- resolution --------------------------------------------------------------


def test_requested_source_defaults_to_config():
    assert requested_source(None, {}) == "auto"
    assert requested_source(None, {"sources": {"source": "builtin"}}) == "builtin"
    assert requested_source("external", {"sources": {"source": "builtin"}}) == "external"


def test_resolve_source_auto_falls_back_to_builtin(tmp_path):
    provider = resolve_source("auto", tmp_path, {"sources": {"source": "auto"}})
    assert isinstance(provider, BuiltinSource)
    assert provider.name == "builtin"


def test_resolve_source_auto_prefers_external(tmp_path):
    _write_external(tmp_path, _external_payload())
    provider = resolve_source("auto", tmp_path, {})
    assert isinstance(provider, ExternalSource)
    assert provider.name == "external"


def test_resolve_source_explicit_builtin_ignores_external(tmp_path):
    _write_external(tmp_path, _external_payload())
    provider = resolve_source("builtin", tmp_path, {})
    assert isinstance(provider, BuiltinSource)


def test_resolve_source_rejects_unknown(tmp_path):
    with pytest.raises(ValueError):
        resolve_source("bogus", tmp_path, {})


def test_external_output_path_override(tmp_path):
    custom = tmp_path / "custom" / "analysis.json"
    custom.parent.mkdir(parents=True)
    custom.write_text("{}", encoding="utf-8")
    found = external_output_path(tmp_path, {"sources": {"external_path": "custom/analysis.json"}})
    assert found == custom


def test_valid_sources_constant():
    assert VALID_SOURCES == ("auto", "external", "builtin")


# --- external collect + hybrid enrichment ------------------------------------


def test_external_source_collect_is_pure(tmp_path):
    _write_external(tmp_path, _external_payload())
    result = ExternalSource(tmp_path, {}).collect()
    assert result.provenance.source == "external"
    assert result.provenance.schema == 1
    assert result.provenance.tool_version == "1.14.0"
    # collect() does not enrich: context-owned sections are filled by the pipeline
    assert "structure" not in result.data
    assert "git" not in result.data


def test_compile_context_enriches_external(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "cli.py").write_text("def main():\n    pass\n", encoding="utf-8")
    _write_external(tmp_path, _external_payload())

    result = compile_context(tmp_path, {}, "external")
    assert result.provenance.source == "external"
    assert result.data["structure"]["modules_count"] == 2
    assert "git" in result.data
    assert "manual_notes" in result.data


def test_external_source_missing_output_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        ExternalSource(tmp_path, {}).collect()


# --- CLI integration ---------------------------------------------------------


def test_context_cli_source_builtin():
    runner = CliRunner()
    with runner.isolated_filesystem():
        pathlib.Path("test.py").write_text("def foo():\n    pass\n", encoding="utf-8")
        result = runner.invoke(cli, ["context", "--no-cache", "--source", "builtin"])
        assert result.exit_code == 0
        assert "Context generated (builtin)" in result.output
        assert pathlib.Path("AI_CONTEXT.md").exists()
        assert pathlib.Path("project_context.json").exists()


def _headings(path: pathlib.Path) -> set:
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    }


def test_external_and_builtin_sections_are_equivalent(tmp_path):
    # Same project, analyzed by both sources: the rendered section set must match.
    proj = tmp_path / "proj"
    (proj / "pkg").mkdir(parents=True)
    (proj / "pkg" / "cli.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (proj / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    _write_external(proj, _external_payload())

    builtin = compile_context(
        proj, {"context": {"sections": ["structure", "metrics", "dependencies", "git"]}}, "builtin"
    )
    external = compile_context(
        proj, {"context": {"sections": ["structure", "metrics", "dependencies", "git"]}}, "external"
    )
    assert external.provenance.source == "external"
    assert builtin.provenance.source == "builtin"

    from ai_context_core.sources.pipeline import render_context

    render_context(
        builtin, proj, {"context": {"sections": ["structure", "metrics", "dependencies", "git"]}}
    )
    builtin_heads = _headings(proj / "AI_CONTEXT.md")
    render_context(
        external, proj, {"context": {"sections": ["structure", "metrics", "dependencies", "git"]}}
    )
    external_heads = _headings(proj / "AI_CONTEXT.md")

    # The configured top-level sections must render for both sources. External
    # legitimately lacks the import-graph sub-sections (it publishes only
    # coupling/circular data), so equality is asserted at the section level.
    core_sections = {
        "## 📁 PROJECT STRUCTURE",
        "## 📈 COMPLEXITY AND METRICS",
        "## 🔗 PRIMARY DEPENDENCIES",
        "## 🔄 GIT AND EVOLUTION",
    }
    assert core_sections <= builtin_heads
    assert core_sections <= external_heads
    # Context-owned sections are equivalent; only analysis-richness differs.
    assert (builtin_heads - external_heads) <= {
        "## 🕸️  DEPENDENCY STRUCTURE",
        "## 🕸️ DEPENDENCY DIAGRAM (Conceptual)",
    }


def test_context_cli_source_external():
    runner = CliRunner()
    with runner.isolated_filesystem():
        root = pathlib.Path(".")
        (root / "pkg").mkdir()
        (root / "pkg" / "cli.py").write_text("def main():\n    pass\n", encoding="utf-8")
        _write_external(root, _external_payload())

        result = runner.invoke(cli, ["context", "--source", "external"])
        assert result.exit_code == 0, result.output
        assert "Context generated (external)" in result.output
        meta = json.loads(pathlib.Path("project_context.json").read_text(encoding="utf-8"))
        assert meta["_meta"]["source"] == "external"
