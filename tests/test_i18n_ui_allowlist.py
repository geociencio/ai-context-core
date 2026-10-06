"""Regression tests for the configurable i18n UI allowlist (Phase 4.1)."""

import ast

from ai_context_core.analyzer.visitors.qgis_visitor import GenericQGISComplianceVisitor


def _i18n_usage(code, **kwargs):
    visitor = GenericQGISComplianceVisitor(**kwargs)
    visitor.visit(ast.parse(code))
    return visitor.results["i18n_usage"]


def test_ui_setter_counts_short_and_camelcase_labels():
    usage = _i18n_usage('label.setText("OK")\nlabel.setTitle("Cancel")\n')
    # Both are user-facing labels the generic heuristics would otherwise reject.
    assert usage["total_strings"] == 2


def test_ui_setter_technical_call_still_ignored():
    usage = _i18n_usage('obj.setObjectName("technical_name")\n')
    assert usage["total_strings"] == 0


def test_ui_allowlist_is_configurable():
    usage = _i18n_usage('label.setLabel("Save")\n', ui_functions={"setLabel"})
    assert usage["total_strings"] == 1


def test_ignored_denylist_is_configurable():
    # Emptying the denylist lets addItem strings fall back to heuristics.
    usage = _i18n_usage('obj.addItem("Item One")\n', ignored_functions=set())
    assert usage["total_strings"] == 1
