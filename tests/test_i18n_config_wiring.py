"""Tests for wiring i18n ignore/UI lists to project config (Phase 4.1 follow-up)."""

import ast

from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.analyzer.visitors.logic import check_qgis_compliance


def test_check_qgis_compliance_reads_tree_i18n_config():
    tree = ast.parse('label.setText("OK")\n')
    tree.i18n_config = {"ui_functions": []}
    assert check_qgis_compliance(tree)["i18n_usage"]["total_strings"] == 0


def test_check_qgis_compliance_defaults_without_config():
    tree = ast.parse('label.setText("OK")\n')
    assert check_qgis_compliance(tree)["i18n_usage"]["total_strings"] == 1


def _module_i18n(analyzer):
    results = analyzer.analyze()
    mod = next(m for m in results["modules"] if m["path"].endswith("mod.py"))
    return mod["qgis_compliance"]["i18n_usage"]


def test_project_config_overrides_ui_allowlist(tmp_path):
    (tmp_path / "mod.py").write_text(
        'def f():\n    obj = None\n    obj.setText("OK")\n', encoding="utf-8"
    )
    analyzer = ProjectAnalyzer(
        str(tmp_path),
        config={"patterns": {"i18n": {"ui_functions": []}}},
        ignore_cache=True,
    )
    assert _module_i18n(analyzer)["total_strings"] == 0


def test_project_config_default_counts_ui_label(tmp_path):
    (tmp_path / "mod.py").write_text(
        'def f():\n    obj = None\n    obj.setText("OK")\n', encoding="utf-8"
    )
    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"patterns": {"i18n": {}}}, ignore_cache=True
    )
    assert _module_i18n(analyzer)["total_strings"] == 1
