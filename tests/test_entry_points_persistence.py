"""Regression tests: entry points must be persisted and rendered (A1)."""

from unittest.mock import patch

from ai_context_core.analyzer.builders.aggregator import ResultsAggregator
from ai_context_core.analyzer.builders.structure import StructureBuilder


def _module(path, entry_type):
    return {
        "path": path,
        "has_main": True,
        "entry_point_info": {"is_entry_point": True, "type": entry_type},
        "syntax_error": False,
        "sloc": 10,
        "lines": 12,
        "functions": [],
        "classes": [],
        "complexity": 1,
        "maintenance_index": 80.0,
    }


def test_aggregate_persists_entry_points(tmp_path):
    module = _module("plugin.py", "qgis_plugin")
    agg = ResultsAggregator(tmp_path, {})

    with (
        patch("ai_context_core.analyzer.builders.dependencies.detect_unused_imports_in_project"),
        patch("ai_context_core.analyzer.builders.formatter.format_complexity_agg"),
        patch("ai_context_core.analyzer.visitors.issues.find_optimizations"),
    ):
        res = agg.aggregate([module], {}, {}, {})

    assert res["entry_points"] == [{"path": "plugin.py", "type": "qgis_plugin"}]


def test_structure_builder_renders_entry_points():
    analyses = {"entry_points": [{"path": "plugin.py", "type": "qgis_plugin"}]}
    lines = []
    StructureBuilder(analyses).build(lines)
    output = "\n".join(lines)

    assert "## 🎯 ENTRY POINTS" in output
    assert "`plugin.py` (qgis_plugin)" in output


def test_structure_builder_supports_legacy_string_entries():
    lines = []
    StructureBuilder({"entry_points": ["old.py"]}).build(lines)
    assert "- `old.py`" in "\n".join(lines)
