"""Aggregation logic for QGIS compliance findings."""

from typing import List, Dict, Any
import re
import fnmatch

_PATTERN_CACHE = {}


def _match_path(path: str, pattern: str) -> bool:
    """Helper to match path against glob pattern robustly using regex and caching.

    Supports recursive ** patterns globally on all Python versions (3.9+).
    """
    # Normalize paths to use forward slashes for consistency
    path = path.replace("\\", "/")
    pattern = pattern.replace("\\", "/")

    if pattern not in _PATTERN_CACHE:
        try:
            if "**" not in pattern:
                # Standard glob behavior for non-recursive patterns
                _PATTERN_CACHE[pattern] = re.compile(fnmatch.translate(pattern))
            else:
                # Convert recursive glob to regex
                # 1. Escape everything
                # 2. Replace escaped **/ with (.*/)? (matches zero or more directories)
                # 3. Replace escaped * with [^/]* (matches within one directory)
                regex_str = (
                    re.escape(pattern)
                    .replace(r"\*\*/", "(.*/)?")
                    .replace(r"\*", "[^/]*")
                )

                # Ensure it matches as a suffix if it doesn't start with a slash/glob
                if not regex_str.startswith("(\\.\\*/)?") and not pattern.startswith(
                    "/"
                ):
                    regex_str = f"^(.*/)?{regex_str}$"
                else:
                    regex_str = f"^{regex_str}$"

                _PATTERN_CACHE[pattern] = re.compile(regex_str)
        except Exception:
            # Fallback if regex generation fails
            return False

    regex = _PATTERN_CACHE[pattern]
    return bool(regex.match(path))


def aggregate_qgis_compliance(
    m_data: List[Dict[str, Any]],
    metadata: Dict[str, Any],
    i18n_config: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Aggregate QGIS-specific results from modules and metadata.

    Args:
        m_data: List of module analysis results
        metadata: Project metadata
        i18n_config: Optional i18n configuration with scope and patterns
    """
    # Default i18n config if not provided
    if i18n_config is None:
        i18n_config = {"scope": "all"}

    scope = i18n_config.get("scope", "all")

    # Determine which modules to include for i18n analysis
    def should_include_for_i18n(module_data: Dict[str, Any]) -> bool:
        """Check if a module should be included in i18n analysis based on scope."""
        if scope == "all":
            return True

        module_path = module_data.get("path", "")
        if not module_path:
            return True  # Include if no path info

        if scope == "gui_only":
            patterns = i18n_config.get(
                "gui_patterns",
                ["gui/**/*.py", "dialogs/**/*.py", "widgets/**/*.py", "ui/**/*.py"],
            )
        elif scope == "custom":
            patterns = i18n_config.get("include_patterns", [])
            exclude_patterns = i18n_config.get("exclude_patterns", [])

            # Check exclusions first
            for pattern in exclude_patterns:
                if _match_path(module_path, pattern):
                    return False
        else:
            return True  # Unknown scope, include all

        # Check inclusions
        for pattern in patterns:
            if _match_path(module_path, pattern):
                return True

        return False

    # Filter modules for i18n counting
    i18n_modules = [m for m in m_data if should_include_for_i18n(m)]

    # New: Aggregate API compatibility issues
    api_issues = {
        "deprecated_calls": [],
        "qt6_incompatibilities": [],
        "best_practice_violations": [],
    }
    for m in m_data:
        comp = m.get("qgis_compliance", {}).get("api_compatibility", {})
        if comp:
            for key in api_issues:
                for issue in comp.get(key, []):
                    issue["module"] = m["path"]
                    api_issues[key].append(issue)

    agg = {
        "metadata": metadata,
        "processing_framework_detected": any(
            m.get("qgis_compliance", {}).get("processing_framework") for m in m_data
        ),
        "i18n_stats": {
            "total_tr": sum(
                m.get("qgis_compliance", {}).get("i18n_usage", {}).get("tr", 0)
                + m.get("qgis_compliance", {}).get("i18n_usage", {}).get("translate", 0)
                for m in i18n_modules
            ),
            "total_strings": sum(
                m.get("qgis_compliance", {})
                .get("i18n_usage", {})
                .get("total_strings", 0)
                for m in i18n_modules
            ),
            "scope": scope,
            "modules_analyzed": len(i18n_modules),
            "modules_total": len(m_data),
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
            "qt6_incompatibilities_count": len(api_issues["qt6_incompatibilities"]),
        },
        "legacy_signals": sum(
            m.get("qgis_compliance", {}).get("signals_slots", {}).get("legacy", 0)
            for m in m_data
        ),
        "api_compatibility": api_issues,
    }

    # Calculate overall QGIS compliance score
    score = metadata.get("compliance_score", 0) * 0.3
    if agg["processing_framework_detected"]:
        score += 15
    if agg["i18n_stats"]["total_strings"] > 0:
        i18n_ratio = agg["i18n_stats"]["total_tr"] / agg["i18n_stats"]["total_strings"]
        score += min(15, i18n_ratio * 30)
    if agg["gdal_style"] == "Correct":
        score += 10
    if agg["qt_transition"]["pyqt5_count"] == 0:
        score += 15
    if not api_issues["deprecated_calls"]:
        score += 10
    if not api_issues["qt6_incompatibilities"]:
        score += 5

    # Penalize for critical metadata issues/inconsistencies
    res_issues = metadata.get("resources", {}).get("issues", [])
    if res_issues:
        score -= min(20, len(res_issues) * 10)

    agg["compliance_score"] = round(max(0, min(100, score)), 1)
    return agg


from .summarizer_base import BaseSummarizer  # noqa: E402


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
            res.append(
                f"- ⚠️ **Deprecated APIs**: {dep_count} calls to obsolete QGIS 3.x APIs"
            )

        violations = api.get("best_practice_violations", [])
        if any(v["name"] == "QSettings" for v in violations):
            res.append(
                "- 💡 **Best Practice**: Use `QgsSettings` instead of `QSettings`"
            )

        if q.get("legacy_signals", 0) > 0:
            res.append(
                f"- ⚠️ **Signals**: {q['legacy_signals']} legacy SIGNAL/SLOT macros detected"
            )

        # Collect all metadata related issues
        all_issues = []
        all_issues.extend(q.get("metadata", {}).get("issues", []))
        all_issues.extend(q.get("metadata", {}).get("resources", {}).get("issues", []))

        if all_issues:
            res.append("\n### 🚩 Metadata Issues:")
            for issue in all_issues[:10]:
                res.append(f"- {issue}")

        return "\n".join(res)
