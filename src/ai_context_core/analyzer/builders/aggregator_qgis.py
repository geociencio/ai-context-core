"""Aggregation logic for QGIS compliance findings."""

from typing import List, Dict, Any

from .qgis_scope import _should_include_for_i18n
from .qgis_processing import has_processing_imports


def _collect_api_issues(
    m_data: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Collect QGIS API compatibility issues across all modules."""
    api_issues: Dict[str, List[Dict[str, Any]]] = {
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
    return api_issues


def _aggregate_i18n_stats(
    i18n_modules: List[Dict[str, Any]],
    all_modules: List[Dict[str, Any]],
    scope: str,
) -> Dict[str, Any]:
    """Aggregate i18n usage statistics for the selected modules."""
    return {
        "total_tr": sum(
            m.get("qgis_compliance", {}).get("i18n_usage", {}).get("tr", 0)
            + m.get("qgis_compliance", {}).get("i18n_usage", {}).get("translate", 0)
            for m in i18n_modules
        ),
        "total_strings": sum(
            m.get("qgis_compliance", {}).get("i18n_usage", {}).get("total_strings", 0)
            for m in i18n_modules
        ),
        "scope": scope,
        "modules_analyzed": len(i18n_modules),
        "modules_total": len(all_modules),
    }


def _compute_compliance_score(
    agg: Dict[str, Any],
    metadata: Dict[str, Any],
    api_issues: Dict[str, List[Dict[str, Any]]],
) -> float:
    """Compute the overall QGIS compliance score from aggregated data."""
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

    return round(max(0, min(100, score)), 1)


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

    # Filter modules for i18n counting and collect API issues
    i18n_modules = [m for m in m_data if _should_include_for_i18n(m, i18n_config, scope)]
    api_issues = _collect_api_issues(m_data)
    processing_detected = any(
        m.get("qgis_compliance", {}).get("processing_framework") for m in m_data
    )

    agg = {
        "metadata": metadata,
        "processing_framework_detected": processing_detected,
        "declares_processing": processing_detected or has_processing_imports(m_data),
        "i18n_stats": _aggregate_i18n_stats(i18n_modules, m_data, scope),
        "gdal_style": (
            "Correct"
            if all(
                m.get("qgis_compliance", {}).get("gdal_import_style") != "Legacy" for m in m_data
            )
            else "Legacy"
        ),
        "qt_transition": {
            "pyqt5_count": sum(
                len(m.get("qgis_compliance", {}).get("qt_transition", {}).get("pyqt5_imports", []))
                for m in m_data
            ),
            "pyqt6_count": sum(
                len(m.get("qgis_compliance", {}).get("qt_transition", {}).get("pyqt6_imports", []))
                for m in m_data
            ),
            "qt6_incompatibilities_count": len(api_issues["qt6_incompatibilities"]),
        },
        "legacy_signals": sum(
            m.get("qgis_compliance", {}).get("signals_slots", {}).get("legacy", 0) for m in m_data
        ),
        "api_compatibility": api_issues,
    }

    # Calculate overall QGIS compliance score
    agg["compliance_score"] = _compute_compliance_score(agg, metadata, api_issues)
    return agg


# Backward-compatible re-export; canonical home is ``qgis_summarizer``.
from .qgis_summarizer import QGISSummarizer  # noqa: E402, F401
