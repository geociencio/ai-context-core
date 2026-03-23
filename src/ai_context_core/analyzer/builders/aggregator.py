"""Aggregation logic for analyzer results.

Extracted from engine.py to reduce complexity and improve modularity.
"""

from typing import List, Dict, Any
import pathlib
import logging
import time
from . import dependencies
from . import calculator as metrics
from . import ai_recommendations
from ..visitors import issues as v_issues

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
        qgis_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Performs a full aggregation of module data and project-level metrics.

        Args:
            m_data: List of individual module analysis results.
            graph_data: Global dependency graph information.
            git_data: Evolution and churn data from git.
            qgis_metadata: Metadata from metadata.txt if available.

        Returns:
            A post-processed results dictionary ready for reporting.
        """
        # Filter out modules with syntax errors for metric calculations
        valid_modules = [m for m in m_data if not m.get("syntax_error")]

        # Dependency analysis
        unused_imports = dependencies.detect_unused_imports_in_project(valid_modules)
        graph_data["unused_imports"] = unused_imports

        # Security aggregation
        security_issues = self._aggregate_security(m_data)

        # QGIS compliance aggregation
        qgis_compliance = self._run_qgis_aggregation(valid_modules, qgis_metadata)

        # Project-level metrics
        entry_points = [m["path"] for m in valid_modules if m.get("has_main")]
        project_metrics = metrics.calculate_project_metrics(
            valid_modules,
            entry_points,
            len([m for m in valid_modules if "test" in m["path"].lower()]),
            self.config,
            {"qgis_compliance": qgis_compliance},
        )

        # AI Recommendations
        recommendations = ai_recommendations.generate_recommendations(
            valid_modules, project_metrics
        )

        # Complexity aggregation (for backward compatibility)
        from .formatter import format_complexity_agg

        complexity_agg = format_complexity_agg(valid_modules, project_metrics)

        # Module-level optimizations
        optimizations = v_issues.find_optimizations(valid_modules)

        return {
            "project_name": self.project_path.name,
            "metrics": project_metrics,
            "complexity": complexity_agg,
            "modules": m_data,
            "dependencies": graph_data,
            "security": security_issues,
            "qgis_compliance": qgis_compliance,
            "optimizations": optimizations,
            "recommendations": recommendations,
            "patterns": self._aggregate_patterns(valid_modules),
            "git": git_data,
            "timestamp": time.time() if "time" in globals() else None,
        }

    def _run_qgis_aggregation(
        self, m_data: List[Dict[str, Any]], metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Runs QGIS aggregation if enabled in config."""
        qgis_enabled = (
            self.config.get("patterns", {})
            .get("qgis_compliance", {})
            .get("enabled", False)
        )
        if not qgis_enabled:
            return {}

        from .aggregator_qgis import aggregate_qgis_compliance

        patterns = self.config.get("patterns", {}) or {}
        i18n_config = patterns.get("i18n", {}) or {}
        return aggregate_qgis_compliance(m_data, metadata, i18n_config)

    def _aggregate_patterns(self, m_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates design patterns from all modules."""
        all_patterns = {}
        for mod in m_data:
            pats = mod.get("patterns", {})
            for name, instances in pats.items():
                if name not in all_patterns:
                    all_patterns[name] = []
                # Add module info to instances
                for inst in instances:
                    inst["module"] = mod["path"]
                all_patterns[name].extend(instances)
        return all_patterns

    def _aggregate_security(self, m_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregates secrets and AST security issues."""
        # Get secrets first (file-based)
        all_security = v_issues.find_secrets(m_data, str(self.project_path))

        # Add AST security issues from module data
        for mod in m_data:
            ast_issues = mod.get("ast_security", [])
            if ast_issues:
                # Find if module already exists in all_security
                found = False
                for existing in all_security:
                    if existing["module"] == mod["path"]:
                        existing["issues"].extend(ast_issues)
                        existing["total_issues"] = len(existing["issues"])
                        found = True
                        break
                if not found:
                    all_security.append(
                        {
                            "module": mod["path"],
                            "issues": ast_issues,
                            "total_issues": len(ast_issues),
                            "max_severity": "high",  # Default for AST issues for now
                        }
                    )
        return all_security

    def _aggregate_qgis_compliance(
        self, m_data: List[Dict[str, Any]], metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Legacy wrapper for QGIS compliance aggregation."""
        from .aggregator_qgis import aggregate_qgis_compliance

        return aggregate_qgis_compliance(m_data, metadata)


# Alias for backward compatibility
ContextAggregator = ResultsAggregator
