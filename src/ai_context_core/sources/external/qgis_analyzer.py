"""Adapter that consumes ``qgis-plugin-analyzer`` output as a context source.

The external tool publishes ``analysis_results/project_context.json`` (schema
version 1). This module maps that payload into the legacy-compatible analysis
dictionary consumed by the context builders. Context-owned fields (structure,
git, manual notes) are intentionally **omitted** so the hybrid pipeline can fill
them from the builtin providers.
"""

import json
import pathlib
from statistics import mean
from typing import Any, Dict, List, Optional

from ...analyzer.builders import formatter, metric_keys
from ...model import AnalysisResult, Provenance
from ..base import current_git_sha, external_output_path


def _map_module(mod: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a single external module entry."""
    lines = mod.get("lines", 0)
    return {
        "path": mod.get("path", "?"),
        "lines": lines,
        "sloc": lines,
        "loc": lines,
        "file_size_kb": mod.get("file_size_kb", 0),
        "complexity": mod.get("complexity", 0),
        "imports": mod.get("imports", []),
        "classes": mod.get("classes", []),
        "functions": mod.get("functions", []),
        "docstrings": mod.get("docstrings", {}),
        "entry_point_info": {"type": "unknown"},
        "has_main": bool(mod.get("has_main", False)),
        "syntax_error": bool(mod.get("syntax_error", False)),
    }


def _sum_lengths(modules: List[Dict[str, Any]], key: str) -> int:
    """Total number of items across a list-valued module key."""
    return sum(len(m.get(key, [])) for m in modules)


def _module_complexities(modules: List[Dict[str, Any]]) -> List[int]:
    """Complexity values for all modules."""
    return [m.get("complexity", 0) for m in modules]


def _map_metrics(ext_metrics: Dict[str, Any], modules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build the canonical project metrics dict from external metrics + modules."""
    complexities = _module_complexities(modules)
    total_lines = ext_metrics.get("total_lines")
    if total_lines is None:
        total_lines = sum(m.get("lines", 0) for m in modules)
    return {
        metric_keys.QUALITY_SCORE: ext_metrics.get("quality_score", 0.0),
        metric_keys.TOTAL_LINES_CODE: total_lines,
        metric_keys.TOTAL_PHYSICAL_LINES: total_lines,
        metric_keys.TOTAL_FUNCTIONS: _sum_lengths(modules, "functions"),
        metric_keys.TOTAL_CLASSES: _sum_lengths(modules, "classes"),
        metric_keys.AVERAGE_COMPLEXITY: mean(complexities) if complexities else 0.0,
        metric_keys.MAX_COMPLEXITY: max(complexities) if complexities else 0,
        metric_keys.AVG_MAINTENANCE_INDEX: ext_metrics.get("maintainability_score", 0.0),
        metric_keys.TEST_FILES_COUNT: ext_metrics.get("test_files_count", 0),
        metric_keys.ENTRY_POINTS_COUNT: sum(1 for m in modules if m.get("has_main")),
        metric_keys.SCORE_BREAKDOWN: [],
    }


def _map_dependencies(semantic: Dict[str, Any]) -> Dict[str, Any]:
    """Map external semantic data into the internal dependency structure."""
    coupling: Dict[str, Any] = {}
    for path, values in semantic.get("coupling_metrics", {}).items():
        fan_in = values.get("fan_in", 0)
        fan_out = values.get("fan_out", 0)
        coupling[path] = {"fan_in": fan_in, "fan_out": fan_out, "cbo": fan_in + fan_out}

    return {
        "internal": [],
        "external": [],
        "third_party": [],
        "files": {},
        "import_graph": {},
        "circular_dependencies": semantic.get("circular_dependencies", []),
        "graph_metrics": {},
        "coupling_metrics": coupling,
        "unused_imports": {},
    }


def _map_entry_points(modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Derive the entry-point list from modules flagged with ``has_main``."""
    return [
        {"path": m["path"], "type": m["entry_point_info"]["type"]}
        for m in modules
        if m.get("has_main")
    ]


def map_project_context(raw: Dict[str, Any], fallback_name: str = "project") -> Dict[str, Any]:
    """Map an external ``project_context.json`` payload to the internal shape.

    Args:
        raw: Parsed external analyzer output.
        fallback_name: Project name to use when the payload omits one.

    Returns:
        A legacy-compatible analysis dictionary (without context-owned sections).
    """
    modules = [_map_module(m) for m in raw.get("modules", [])]
    metrics = _map_metrics(raw.get("metrics", {}), modules)
    project_name = raw.get("project_name") or fallback_name

    return {
        "project_name": project_name,
        "metrics": metrics,
        "complexity": formatter.format_complexity_agg(modules, metrics),
        "modules": modules,
        "dependencies": _map_dependencies(raw.get("semantic", {})),
        "security": raw.get("security", {}).get("findings", []),
        "qgis_compliance": raw.get("qgis_compliance", {}),
        "recommendations": [],
        "patterns": {},
        "antipatterns": [],
        "optimizations": [],
        "entry_points": _map_entry_points(modules),
        "timestamp": None,
    }


class ExternalSource:
    """Read analysis results produced by ``qgis-plugin-analyzer``."""

    name = "external"

    def __init__(self, project_path: pathlib.Path, config: Optional[Dict[str, Any]] = None):
        """Initialize the external source.

        Args:
            project_path: Project root.
            config: Analyzer configuration; ``[sources].external_path`` overrides
                the default output location.
        """
        self.project_path = pathlib.Path(project_path).resolve()
        self.config = config or {}

    def collect(self) -> AnalysisResult:
        """Read and map the external analyzer output.

        Raises:
            FileNotFoundError: When no external output is available.
        """
        path = external_output_path(self.project_path, self.config)
        if path is None:
            raise FileNotFoundError(
                "No external analyzer output found at "
                "analysis_results/project_context.json (run qgis-analyzer first)."
            )
        raw = json.loads(path.read_text(encoding="utf-8"))
        data = map_project_context(raw, fallback_name=self.project_path.name)
        return AnalysisResult(
            data=data,
            provenance=Provenance(
                source=self.name,
                schema=raw.get("schema_version"),
                tool_version=raw.get("analyzer_version"),
                git_sha=current_git_sha(self.project_path),
            ),
        )
