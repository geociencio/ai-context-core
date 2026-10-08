"""Contract tests for deprecated in-module aliases."""

import importlib
import warnings


def test_deprecated_aliases_warn_on_access():
    aggregator = importlib.import_module("ai_context_core.analyzer.builders.aggregator")
    ast_qgis = importlib.import_module("ai_context_core.analyzer.visitors.ast_qgis")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert aggregator.ContextAggregator is aggregator.ResultsAggregator
        assert ast_qgis.QGISComplianceVisitor is ast_qgis.GenericQGISComplianceVisitor

    deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert len(deprecations) >= 2
