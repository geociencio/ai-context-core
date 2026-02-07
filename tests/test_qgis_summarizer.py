from ai_context_core.analyzer.summarizers.qgis import QGISSummarizer


def test_qgis_summarizer_full_coverage():
    analyses = {
        "qgis_compliance": {
            "compliance_score": 85.5,
            "processing_framework_detected": True,
            "i18n_stats": {"total_tr": 8, "total_strings": 10},
            "qt_transition": {"pyqt5_count": 3},
            "gdal_style": "Legacy",
            "legacy_signals": 5,
            "metadata": {"issues": ["Missing description", "Invalid version"]},
        }
    }
    summarizer = QGISSummarizer(analyses)
    summary = summarizer.build()

    assert "85.5/100" in summary
    assert "Processing Framework detected" in summary
    assert "80.0%" in summary
    assert "3 PyQt5 imports" in summary
    assert "Legacy imports detected" in summary
    assert "5 legacy SIGNAL/SLOT" in summary
    assert "Missing description" in summary


def test_qgis_summarizer_empty():
    summarizer = QGISSummarizer({})
    assert summarizer.build() == ""


def test_qgis_summarizer_no_processing():
    analyses = {"qgis_compliance": {"processing_framework_detected": False}}
    summarizer = QGISSummarizer(analyses)
    summary = summarizer.build()
    assert "No Processing Algorithms found" in summary
