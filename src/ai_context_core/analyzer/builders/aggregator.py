"""Aggregation logic for analyzer results.

Context-only (v5.0.0): security, QGIS compliance, design patterns and
anti-patterns are no longer aggregated; those domains belong to
``qgis-plugin-analyzer``.
"""

import logging
import pathlib
from typing import Any, Dict, List

from . import calculator as metrics
from . import dependencies
from . import metric_keys
from ..providers.fs_scanner import count_test_files
from ..visitors.issues import find_optimizations

logger = logging.getLogger(__name__)


class ResultsAggregator:
    """Aggregates and post-processes analysis results from multiple modules."""

    def __init__(self, project_path: pathlib.Path, config: Dict[str, Any]):
        """Initialize the aggregator.

        Args:
            project_path: Path to the project root.
            config: Configuration dictionary for metrics and thresholds.
        """
        self.project_path = project_path
        self.config = config

    def aggregate(
        self,
        m_data: List[Dict[str, Any]],
        graph_data: Dict[str, Any],
        git_data: Dict[str, Any],
        _qgis_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Perform a full aggregation of module data and project-level metrics.

        Args:
            m_data: List of individual module analysis results.
            graph_data: Global dependency graph information.
            git_data: Evolution and churn data from git.
            _qgis_metadata: Unused; retained for call-site compatibility.

        Returns:
            A post-processed results dictionary ready for reporting.
        """
        valid_modules = [m for m in m_data if not m.get("syntax_error")]

        # Dependency analysis
        unused_imports = dependencies.detect_unused_imports_in_project(valid_modules, self.config)
        graph_data["unused_imports"] = unused_imports

        # Project-level metrics
        entry_point_modules = [m for m in valid_modules if m.get("has_main")]
        entry_points = [m["path"] for m in entry_point_modules]
        entry_points_detail = [
            {
                "path": m["path"],
                "type": m.get("entry_point_info", {}).get("type") or "unknown",
            }
            for m in entry_point_modules
        ]
        test_files_count = count_test_files(self.project_path)
        project_metrics = metrics.calculate_project_metrics(
            valid_modules,
            entry_points,
            test_files_count,
            self.config,
            {},
        )

        missing = metric_keys.missing_metric_keys(project_metrics)
        if missing:
            logger.warning("Missing project metric keys: %s", missing)

        from .formatter import format_complexity_agg

        complexity_agg = format_complexity_agg(valid_modules, project_metrics)
        optimizations = find_optimizations(valid_modules, self.config)

        return {
            "project_name": self.project_path.name,
            "metrics": project_metrics,
            "complexity": complexity_agg,
            "modules": m_data,
            "dependencies": graph_data,
            "optimizations": optimizations,
            "entry_points": entry_points_detail,
            "git": git_data,
            "timestamp": None,
        }


def __getattr__(name: str):
    """Warn on access to deprecated aliases (PEP 562)."""
    if name == "ContextAggregator":
        from ai_context_core.deprecations import warn_deprecated

        warn_deprecated(
            "ai_context_core.analyzer.builders.aggregator.ContextAggregator",
            "ai_context_core.analyzer.builders.aggregator.ResultsAggregator",
        )
        return ResultsAggregator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
