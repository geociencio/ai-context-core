"""QGIS standards compliance section builder."""

from .summarizer_base import BaseSummarizer


class QGISSummarizer(BaseSummarizer):
    """Builds the QGIS standards compliance section."""

    def build(self) -> str:
        q = self.analyses.get("qgis_compliance", {})
        if not q:
            return ""
        res = [f"- **Compliance Score**: {q.get('compliance_score', 0):.1f}/100"]

        resources = q.get("metadata", {}).get("resources", {})
        if resources:
            qrc_count = len(resources.get("resource_files", []))
            if qrc_count > 0:
                res.append(f"- 📦 **Resources**: {qrc_count} `.qrc` files detected")

            if resources.get("metadata", {}).get("name"):
                res.append(
                    f"- ℹ️ **Plugin**: {resources['metadata']['name']} (v{resources['metadata'].get('version', '?')})"
                )

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
            res.append(
                f"- 🍎 **Qt6 Transition**: {qt['pyqt5_count']} PyQt5 imports (Critical for QGIS 4)"
            )

        qt6_inc = qt.get("qt6_incompatibilities_count", 0)
        if qt6_inc > 0:
            res.append(
                f"- 🚩 **QGIS 4.x Risks**: {qt6_inc} incompatible patterns detected (SIGNAL/SLOT macros)"
            )

        if q.get("gdal_style") == "Legacy":
            res.append("- ⚠️ **GDAL Style**: Legacy imports detected (`import gdal`)")

        api = q.get("api_compatibility", {})
        dep_count = len(api.get("deprecated_calls", []))
        if dep_count > 0:
            res.append(f"- ⚠️ **Deprecated APIs**: {dep_count} calls to obsolete QGIS 3.x APIs")

        violations = api.get("best_practice_violations", [])
        if any(v["name"] == "QSettings" for v in violations):
            res.append("- 💡 **Best Practice**: Use `QgsSettings` instead of `QSettings`")

        if q.get("legacy_signals", 0) > 0:
            res.append(f"- ⚠️ **Signals**: {q['legacy_signals']} legacy SIGNAL/SLOT macros detected")

        # Collect all metadata related issues
        all_issues = []
        all_issues.extend(q.get("metadata", {}).get("issues", []))
        all_issues.extend(q.get("metadata", {}).get("resources", {}).get("issues", []))

        if all_issues:
            res.append("\n### 🚩 Metadata Issues:")
            for issue in all_issues[:10]:
                res.append(f"- {issue}")

        return "\n".join(res)
