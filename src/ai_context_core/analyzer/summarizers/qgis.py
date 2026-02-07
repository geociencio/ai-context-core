"""Summarizers for QGIS-specific metrics."""

from .base import BaseSummarizer

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
            res.append("- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)")

        i18n = q.get("i18n_stats", {})
        if i18n.get("total_strings", 0) > 0:
            cov = (i18n["total_tr"] / i18n["total_strings"]) * 100
            res.append(
                f"- **i18n Coverage**: {cov:.1f}% ({i18n['total_tr']}/{i18n['total_strings']} strings)"
            )

        qt = q.get("qt_transition", {})
        if qt.get("pyqt5_count", 0) > 0:
            res.append(f"- 🍎 **Qt6 Transition**: {qt['pyqt5_count']} PyQt5 imports (Action required for QGIS 4)")

        if q.get("gdal_style") == "Legacy":
            res.append("- ⚠️ **GDAL Style**: Legacy imports detected (`import gdal`)")

        if q.get("legacy_signals", 0) > 0:
            res.append(f"- ⚠️ **Signals**: {q['legacy_signals']} legacy SIGNAL/SLOT macros detected")

        issues = q.get("metadata", {}).get("issues", [])
        if issues:
            res.append("\n### 🚩 Metadata Issues:")
            for issue in issues[:5]:
                res.append(f"- {issue}")

        return "\n".join(res)
