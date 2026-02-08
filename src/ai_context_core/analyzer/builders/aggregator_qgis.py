"""Aggregation logic for QGIS compliance findings."""

from typing import List, Dict, Any


def aggregate_qgis_compliance(
    m_data: List[Dict[str, Any]], metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Aggregate QGIS-specific results from modules and metadata."""
    agg = {
        "metadata": metadata,
        "processing_framework_detected": any(
            m.get("qgis_compliance", {}).get("processing_framework") for m in m_data
        ),
        "i18n_stats": {
            "total_tr": sum(
                m.get("qgis_compliance", {}).get("i18n_usage", {}).get("tr", 0)
                + m.get("qgis_compliance", {}).get("i18n_usage", {}).get("translate", 0)
                for m in m_data
            ),
            "total_strings": sum(
                m.get("qgis_compliance", {})
                .get("i18n_usage", {})
                .get("total_strings", 0)
                for m in m_data
            ),
        },
        "gdal_style": (
            "Correct"
            if all(
                m.get("qgis_compliance", {}).get("gdal_import_style") != "Legacy"
                for m in m_data
            )
            else "Legacy"
        ),
        "qt_transition": {
            "pyqt5_count": sum(
                len(
                    m.get("qgis_compliance", {})
                    .get("qt_transition", {})
                    .get("pyqt5_imports", [])
                )
                for m in m_data
            ),
            "pyqt6_count": sum(
                len(
                    m.get("qgis_compliance", {})
                    .get("qt_transition", {})
                    .get("pyqt6_imports", [])
                )
                for m in m_data
            ),
        },
        "legacy_signals": sum(
            m.get("qgis_compliance", {}).get("signals_slots", {}).get("legacy", 0)
            for m in m_data
        ),
    }

    # Calculate overall QGIS compliance score
    score = metadata.get("compliance_score", 0) * 0.4
    if agg["processing_framework_detected"]:
        score += 20
    if agg["i18n_stats"]["total_strings"] > 0:
        i18n_ratio = agg["i18n_stats"]["total_tr"] / agg["i18n_stats"]["total_strings"]
        score += min(20, i18n_ratio * 40)
    if agg["gdal_style"] == "Correct":
        score += 10
    if agg["qt_transition"]["pyqt5_count"] == 0:
        score += 10

    agg["compliance_score"] = round(min(100, score), 1)
    return agg


from .summarizer_base import BaseSummarizer  # noqa: E402


class QGISSummarizer(BaseSummarizer):
    """Builds the QGIS standards compliance section."""

    def build(self) -> str:
        q = self.analyses.get("qgis_compliance", {})
        if not q:
            return ""
        res = [f"- **Compliance Score**: {q.get('compliance_score', 0):.1f}/100"]

        if q.get("processing_framework_detected"):
            res.append("- ✅ **Architecture**: Processing Framework detected")
        else:
            res.append(
                "- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)"
            )

        i18n = q.get("i18n_stats", {})
        if i18n.get("total_strings", 0) > 0:
            cov = (i18n["total_tr"] / i18n["total_strings"]) * 100
            res.append(
                f"- **i18n Coverage**: {cov:.1f}% ({i18n['total_tr']}/{i18n['total_strings']} strings)"
            )

        qt = q.get("qt_transition", {})
        if qt.get("pyqt5_count", 0) > 0:
            res.append(
                f"- 🍎 **Qt6 Transition**: {qt['pyqt5_count']} PyQt5 imports (Action required for QGIS 4)"
            )

        if q.get("gdal_style") == "Legacy":
            res.append("- ⚠️ **GDAL Style**: Legacy imports detected (`import gdal`)")

        if q.get("legacy_signals", 0) > 0:
            res.append(
                f"- ⚠️ **Signals**: {q['legacy_signals']} legacy SIGNAL/SLOT macros detected"
            )

        issues = q.get("metadata", {}).get("issues", [])
        if issues:
            res.append("\n### 🚩 Metadata Issues:")
            for issue in issues[:5]:
                res.append(f"- {issue}")

        return "\n".join(res)
