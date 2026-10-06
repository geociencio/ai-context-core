"""Contract tests for deprecated compatibility facades (Phase 3)."""

import importlib
import warnings

import pytest

# (deprecated path, canonical replacement)
DEPRECATED_FACADES = [
    (
        "ai_context_core.analyzer.patterns_detectors.singleton",
        "ai_context_core.analyzer.visitors.singleton",
    ),
    (
        "ai_context_core.analyzer.context_builders.structure",
        "ai_context_core.analyzer.builders.structure",
    ),
    (
        "ai_context_core.commands.clean",
        "ai_context_core.cli.commands.clean",
    ),
    (
        "ai_context_core.cli_groups.specialized",
        "ai_context_core.cli.commands.specialized",
    ),
]


@pytest.mark.parametrize(("old", "new"), DEPRECATED_FACADES)
def test_deprecated_facade_warns_and_reexports(old, new):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        module = importlib.import_module(old)
        importlib.reload(module)

    assert any(
        issubclass(w.category, DeprecationWarning) and "deprecated" in str(w.message)
        for w in caught
    )

    canonical = importlib.import_module(new)
    for name in getattr(module, "__all__", []):
        assert getattr(module, name) is getattr(canonical, name)


def test_deprecated_aliases_warn_on_access():
    aggregator = importlib.import_module(
        "ai_context_core.analyzer.builders.aggregator"
    )
    ast_qgis = importlib.import_module("ai_context_core.analyzer.visitors.ast_qgis")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert aggregator.ContextAggregator is aggregator.ResultsAggregator
        assert ast_qgis.QGISComplianceVisitor is ast_qgis.GenericQGISComplianceVisitor

    deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert len(deprecations) >= 2
