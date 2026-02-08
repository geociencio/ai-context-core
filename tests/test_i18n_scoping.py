import pytest
from ai_context_core.analyzer.builders.aggregator_qgis import aggregate_qgis_compliance


@pytest.fixture
def mock_modules():
    return [
        {
            "file": "/project/gui/dialog.py",
            "qgis_compliance": {
                "i18n_usage": {"tr": 10, "translate": 0, "total_strings": 20},
                "processing_framework": False,
                "gdal_import_style": "Modern",
                "qt_transition": {"pyqt5_imports": [], "pyqt6_imports": []},
                "signals_slots": {"legacy": 0, "modern": 0},
            },
        },
        {
            "file": "/project/core/logic.py",
            "qgis_compliance": {
                # Untranslated technical strings
                "i18n_usage": {"tr": 0, "translate": 0, "total_strings": 50},
                "processing_framework": False,
                "gdal_import_style": "Modern",
                "qt_transition": {"pyqt5_imports": [], "pyqt6_imports": []},
                "signals_slots": {"legacy": 0, "modern": 0},
            },
        },
    ]


@pytest.fixture
def base_metadata():
    return {"compliance_score": 100}


def test_scope_all_default(mock_modules, base_metadata):
    """Test default behavior processes all modules."""
    agg = aggregate_qgis_compliance(mock_modules, base_metadata, {"scope": "all"})

    stats = agg["i18n_stats"]
    assert stats["total_strings"] == 70  # 20 + 50
    assert stats["total_tr"] == 10

    # 10/70 = 14.2% coverage
    i18n_ratio = 10 / 70
    expected_score = (
        40 + 10 + 10 + min(20, i18n_ratio * 40)
    )  # Base 40 + GDAL 10 + Qt 10 + i18n
    assert agg["compliance_score"] == pytest.approx(expected_score, 0.1)


def test_scope_gui_only(mock_modules, base_metadata):
    """Test gui_only scope filters out core modules."""
    config = {"scope": "gui_only", "gui_patterns": ["gui/**/*.py"]}
    agg = aggregate_qgis_compliance(mock_modules, base_metadata, config)

    stats = agg["i18n_stats"]
    assert stats["total_strings"] == 20  # Only GUI file counted
    assert stats["total_tr"] == 10
    assert stats["modules_analyzed"] == 1

    # 10/20 = 50% coverage -> Higher score
    i18n_ratio = 10 / 20
    expected_score = 40 + 10 + 10 + min(20, i18n_ratio * 40)
    assert agg["compliance_score"] == pytest.approx(expected_score, 0.1)

    # Verify score improved with filtering
    raw_agg = aggregate_qgis_compliance(mock_modules, base_metadata, {"scope": "all"})
    assert agg["compliance_score"] > raw_agg["compliance_score"]


def test_scope_custom(mock_modules, base_metadata):
    """Test custom patterns."""
    config = {
        "scope": "custom",
        "include_patterns": ["core/**/*.py"],
        "exclude_patterns": [],
    }
    agg = aggregate_qgis_compliance(mock_modules, base_metadata, config)

    stats = agg["i18n_stats"]
    assert stats["total_strings"] == 50  # Only Core file counted
    assert stats["total_tr"] == 0

    assert agg["compliance_score"] < 70  # Should be low due to 0% i18n


def test_backward_compatibility(mock_modules, base_metadata):
    """Test calling without config works like 'all'."""
    agg = aggregate_qgis_compliance(mock_modules, base_metadata)

    assert agg["i18n_stats"]["total_strings"] == 70
    assert agg["i18n_stats"]["scope"] == "all"
