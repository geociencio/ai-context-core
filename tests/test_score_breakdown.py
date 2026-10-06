"""Regression tests for the explainable, configurable Quality Score (Phase 2)."""

from ai_context_core.analyzer.builders.calculator import calculate_project_metrics
from ai_context_core.analyzer.builders.metric_keys import (
    PROJECT_METRIC_KEYS,
    QUALITY_SCORE,
    SCORE_BREAKDOWN,
)
from ai_context_core.analyzer.builders.metrics_summarizer import MetricsSummarizer


def _modules(complexity=30, mi=90.0):
    return [
        {
            "path": "a.py",
            "sloc": 10,
            "lines": 12,
            "functions": [],
            "classes": [],
            "complexity": complexity,
            "maintenance_index": mi,
        }
    ]


def test_score_breakdown_is_canonical_and_explains_score():
    metrics = calculate_project_metrics(_modules(), [], 1, {})
    breakdown = metrics[SCORE_BREAKDOWN]

    assert SCORE_BREAKDOWN in PROJECT_METRIC_KEYS
    assert set(breakdown) == {
        "base",
        "complexity",
        "max_complexity",
        "maintainability",
        "tests",
    }
    expected = max(0.0, min(100.0, sum(breakdown.values())))
    assert metrics[QUALITY_SCORE] == expected
    assert breakdown["complexity"] == -30.0
    assert breakdown["max_complexity"] == -2.5


def test_high_complexity_threshold_is_configurable():
    default = calculate_project_metrics(_modules(), [], 1, {})[SCORE_BREAKDOWN]
    relaxed = calculate_project_metrics(
        _modules(), [], 1, {"scoring": {"complexity_high_threshold": 100}}
    )[SCORE_BREAKDOWN]

    assert default["max_complexity"] < 0
    assert relaxed["max_complexity"] == 0


def test_legacy_thresholds_still_apply():
    metrics = calculate_project_metrics(
        _modules(), [], 1, {"thresholds": {"complexity_medium": 100}}
    )
    assert metrics[SCORE_BREAKDOWN]["complexity"] == 0


def test_metrics_summarizer_renders_breakdown_and_note():
    metrics = calculate_project_metrics(_modules(), [], 1, {})
    analyses = {"metrics": metrics, "complexity": {}, "structure": {}}
    output = MetricsSummarizer(analyses).build_metrics()

    assert "Score Breakdown" in output
    assert "non-canonical" in output
    assert "Complexity (max)" in output
