"""Regression guard for the repository's own analysis scope and score (Phase S)."""

import pathlib

from ai_context_core.analyzer.builders import calculator, metric_keys
from ai_context_core.analyzer.providers.config_loader import load_config
from ai_context_core.analyzer.providers import fs_utils, worker
from ai_context_core.analyzer.providers.fs_scanner import count_test_files

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Modules above this budget trigger the max-complexity outlier penalty.
COMPLEXITY_BUDGET = 25


def _analyze_scope():
    """Analyze the repo's own scope sequentially, without writing artifacts."""
    cfg = load_config(ROOT)
    scan = fs_utils.scan_project(ROOT, [])
    analyzer = worker.AnalysisWorker(ROOT, cfg, 1, {})
    modules = [analyzer.analyze_single(f) for f in scan.python_files]
    valid = [m for m in modules if m and not m.get("syntax_error")]
    return valid, cfg


def test_no_source_module_exceeds_complexity_budget():
    valid, _ = _analyze_scope()
    over = [
        (m["path"], m.get("complexity"))
        for m in valid
        if m.get("complexity", 0) > COMPLEXITY_BUDGET
    ]
    assert over == [], f"modules above the complexity budget: {over}"


def test_self_quality_score_has_no_outlier_penalty():
    valid, cfg = _analyze_scope()
    entry_points = [m["path"] for m in valid if m.get("has_main")]
    metrics = calculator.calculate_project_metrics(
        valid, entry_points, count_test_files(ROOT), cfg, {"qgis_compliance": {}}
    )

    assert metrics[metric_keys.SCORE_BREAKDOWN]["max_complexity"] == 0
    # Removed high-MI facade shims lowered the average-based maintainability,
    # so the heuristic score baseline moved from >=95 to ~90.
    assert metrics[metric_keys.QUALITY_SCORE] >= 90
