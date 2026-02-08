import pathlib
from unittest.mock import patch
from ai_context_core.analyzer.aggregator import ResultsAggregator


def test_aggregate_security_combined():
    # Coverage for aggregator.py lines 139-143
    # Case: A module has both a secret and an AST security issue
    aggregator = ResultsAggregator(pathlib.Path("/tmp/proj"), {})

    # Mock issues.find_secrets to return a finding for 'mod1.py'
    m_data = [
        {
            "path": "mod1.py",
            "ast_security": [{"description": "AST issue", "severity": "high"}],
            "syntax_error": False,
        }
    ]

    with patch("ai_context_core.analyzer.builders.issues.find_secrets") as mock_secrets:
        mock_secrets.return_value = [
            {
                "module": "mod1.py",
                "issues": [{"description": "Secret found", "severity": "critical"}],
                "total_issues": 1,
                "max_severity": "critical",
            }
        ]

        res = aggregator._aggregate_security(m_data)

        assert len(res) == 1
        assert res[0]["module"] == "mod1.py"
        # Should have both secret and AST issue
        assert len(res[0]["issues"]) == 2
        assert res[0]["total_issues"] == 2


def test_legacy_qgis_aggregation_wrapper():
    # Coverage for aggregator.py lines 159-161
    aggregator = ResultsAggregator(pathlib.Path("/tmp/proj"), {})
    m_data = [{"path": "m.py"}]
    metadata = {"compliance_score": 100}

    with patch(
        "ai_context_core.analyzer.builders.aggregator_qgis.aggregate_qgis_compliance"
    ) as mock_agg:
        mock_agg.return_value = {"score": 100}
        res = aggregator._aggregate_qgis_compliance(m_data, metadata)
        assert res["score"] == 100
        mock_agg.assert_called_once_with(m_data, metadata)


def test_qgis_aggregation_processing_framework():
    # Coverage for aggregator_components/qgis.py line 63
    from ai_context_core.analyzer.builders.aggregator_qgis import (
        aggregate_qgis_compliance,
    )

    m_data = [
        {
            "qgis_compliance": {
                "processing_framework": True,
                "i18n_usage": {"total_strings": 0},
                "qt_transition": {"pyqt5_imports": []},
                "gdal_import_style": "Correct",
            }
        }
    ]
    metadata = {"compliance_score": 100}
    # score = 100 * 0.4 = 40
    # + 20 (processing) = 60
    # + 10 (gdal) = 70
    # + 10 (qt) = 80
    res = aggregate_qgis_compliance(m_data, metadata)
    assert res["compliance_score"] == 80.0
    assert res["processing_framework_detected"] is True


def test_aggregator_timestamp():
    # Coverage for aggregator.py line 94
    agg = ResultsAggregator(
        pathlib.Path("/tmp/proj"), {"patterns": {"qgis_compliance": {"enabled": False}}}
    )
    # Mocking dependencies etc to make aggregate run
    with (
        patch("ai_context_core.analyzer.dependencies.detect_unused_imports_in_project"),
        patch("ai_context_core.analyzer.metrics.calculate_project_metrics"),
        patch("ai_context_core.analyzer.ai_recommendations.generate_recommendations"),
        patch("ai_context_core.analyzer.builders.formatter.format_complexity_agg"),
        patch("ai_context_core.analyzer.issues.find_optimizations"),
        patch("ai_context_core.analyzer.issues.find_secrets"),
    ):
        res = agg.aggregate([], {}, {}, {})
        assert "timestamp" in res
        assert isinstance(res["timestamp"], float)
