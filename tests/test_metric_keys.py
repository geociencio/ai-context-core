from ai_context_core.analyzer.builders.calculator import calculate_project_metrics
from ai_context_core.analyzer.builders.formatter import format_complexity_agg
from ai_context_core.analyzer.builders.metric_keys import (
    PROJECT_METRIC_KEYS,
    missing_metric_keys,
)


def _modules():
    return [
        {
            "path": "a.py",
            "sloc": 100,
            "lines": 120,
            "functions": [{"name": "f"}],
            "classes": [{"name": "C"}],
            "complexity": 5,
            "maintenance_index": 60.0,
        },
        {
            "path": "b.py",
            "sloc": 50,
            "lines": 55,
            "functions": [],
            "classes": [],
            "complexity": 3,
            "maintenance_index": 70.0,
        },
    ]


def test_calculate_project_metrics_returns_canonical_keys_only():
    metrics = calculate_project_metrics(_modules(), ["a.py"], 1, {})

    assert set(metrics) == set(PROJECT_METRIC_KEYS)
    assert "avg_complexity" not in metrics
    assert "avg_maintainability" not in metrics
    assert "average_complexity" in metrics
    assert "avg_maintenance_index" in metrics


def test_metric_contract_calculator_to_formatter():
    metrics = calculate_project_metrics(_modules(), ["a.py"], 1, {})
    agg = format_complexity_agg(_modules(), metrics)

    assert agg["average_complexity"] == metrics["average_complexity"]
    assert agg["avg_maintenance_index"] == metrics["avg_maintenance_index"]
    assert agg["total_functions"] == metrics["total_functions"]
    assert agg["total_classes"] == metrics["total_classes"]
    assert agg["total_lines"] == metrics["total_lines_code"]
    assert agg["total_physical_lines"] == metrics["total_physical_lines"]


def test_missing_metric_keys_reports_gaps():
    assert sorted(missing_metric_keys({})) == sorted(PROJECT_METRIC_KEYS)

    full = calculate_project_metrics(_modules(), ["a.py"], 1, {})
    assert missing_metric_keys(full) == []
