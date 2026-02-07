"""Main orchestration engine for project analysis.

The ProjectAnalyzer coordinates the analysis of multiple Python modules,
aggregating results from AST analysis, dependency checking, and issue detection.
"""

import logging
import time
import pathlib
import json
from typing import Dict, Any, List, Optional
from . import (
    fs_utils,
    reporting,
    dependencies,
    git_analysis,
    aggregator,
)
from ..context.manager import AIContextManager

logger = logging.getLogger(__name__)


try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def load_config(root_path: pathlib.Path) -> Dict[str, Any]:
    """Load configuration from defaults.toml and optional project overrides.

    Adheres to zero-dependency policy by using stdlib tomllib (Py3.11+)
    or optional tomli. If neither is available, falls back to hardcoded defaults.

    Args:
        root_path: Project root path to look for override config.

    Return:
        Merged configuration dictionary.

    """
    # Load defaults from package
    default_config = {}
    if tomllib:
        try:
            defaults_path = (
                pathlib.Path(__file__).parent / ".." / "config" / "defaults.toml"
            )
            if defaults_path.exists():
                with open(defaults_path, "rb") as f:
                    default_config = tomllib.load(f)
        except Exception as e:
            logger.warning(f"Failed to load defaults.toml: {e}")

    if not default_config:
        # Fallback if TOML parsing fails or fails to load
        return _get_hardcoded_defaults()

    # Load overrides from project
    override_config = {}
    if tomllib:
        try:
            project_config_path = root_path / ".ai-context" / "config.toml"
            if project_config_path.exists():
                with open(project_config_path, "rb") as f:
                    override_config = tomllib.load(f)
        except Exception as e:
            logger.warning(f"Failed to load project config.toml: {e}")

    # Merge configs (shallow merge for now, or recursive if needed)
    # Simple recursive merge for top-level keys
    final_config = default_config.copy()
    for section, values in override_config.items():
        if isinstance(values, dict) and section in final_config:
            final_config[section].update(values)
        else:
            final_config[section] = values

    return final_config


def _get_hardcoded_defaults() -> Dict[str, Any]:
    """Return fallback hardcoded configuration.

    Returns:
        Dictionary with default quality weights and thresholds.
    """
    return {
        "quality_weights": {
            "docstrings": 30,
            "complexity_low": 20,
            "size_small": 15,
            "has_main": 5,
            "no_syntax_error": 30,
            "complexity_medium": 10,
            "complexity_high": -10,
            "size_medium": 10,
        },
        "thresholds": {
            "complexity_low": 5,
            "complexity_medium": 15,
            "complexity_high": 25,
            "size_small": 200,
            "size_medium": 500,
        },
    }


class ProjectAnalyzer:
    """Optimized and modular Python project analyzer.

    Coordinates scanning, analysis, and aggregation of project data.
    """

    def __init__(
        self,
        project_path: str,
        config: Optional[Dict[str, Any]] = None,
        max_workers: Optional[int] = None,
        exclude_patterns: Optional[List[str]] = None,
        ignore_cache: bool = False,
    ):
        """Initialize the analyzer with project settings.

        Args:
            project_path: Absolute or relative path to the project root.
            config: Optional configuration dictionary.
            max_workers: Maximum number of parallel workers for analysis.
            exclude_patterns: List of glob patterns to exclude from scanning.
            ignore_cache: Whether to force a full analysis ignoring existing cache.
        """
        from .engine_components import load_config as loader_func

        self.project_path = pathlib.Path(project_path).resolve()
        self.max_workers = max_workers or (
            2 * (4 if hasattr(time, "get_clock_info") else 1)
        )
        self.config = config or loader_func(self.project_path)

        self.exclusion_patterns = fs_utils.load_exclusion_patterns(
            self.project_path, exclude_patterns
        )
        self.context_manager = AIContextManager(project_path)
        self.analysis_cache = (
            {} if ignore_cache else fs_utils.load_cache(self.project_path)
        )
        self.error_log = {}

    def analyze(self, output_format: str = "markdown") -> Dict[str, Any]:
        """Execute the complete project analysis pipeline.

        Orchestrates scanning, parallel module analysis, dependency graph building,
        git evolution tracking, and results aggregation.

        Args:
            output_format: Desired report format ('markdown' or 'html').

        Returns:
            A comprehensive dictionary containing all analysis results.
        """
        start_time = time.time()
        logger.info(f"Starting analysis for {self.project_path}")

        # 1. Scanning and Parallel Analysis
        from .engine_components import AnalysisWorker

        scan_res = fs_utils.scan_project(self.project_path, self.exclusion_patterns)
        worker = AnalysisWorker(
            self.project_path, self.config, self.max_workers, self.analysis_cache
        )
        modules_data = worker.run_parallel(scan_res.python_files)
        self.error_log.update(worker.error_log)

        # 2. Dependency Analysis
        dep_analyzer = dependencies.DependencyAnalyzer(self.project_path)
        graph_data = dep_analyzer.build_graph(modules_data)

        # 3. Evolution analysis (Git)
        git_data = git_analysis.analyze_git_evolution(self.project_path)

        # 4. Aggregate results
        qgis_metadata = fs_utils.parse_qgis_metadata(self.project_path)
        agg = aggregator.ResultsAggregator(self.project_path, self.config)
        results = agg.aggregate(modules_data, graph_data, git_data, qgis_metadata)

        # Add tree structure and manual notes
        results["structure"] = {
            "tree": fs_utils.generate_tree_optimized(self.project_path),
            "modules_count": len(modules_data),
            "file_types": scan_res.file_types,
            "size_stats": scan_res.size_stats,
        }
        results["manual_notes"] = self._read_manual_notes()

        # 5. Finalization
        self._generate_outputs(results, output_format)
        fs_utils.save_cache(self.project_path, self.analysis_cache)

        logger.info(f"Analysis completed in {time.time() - start_time:.2f}s")
        return results

    def _read_manual_notes(self) -> str:
        """Read manual architecture notes if they exist."""
        notes_path = self.project_path / ".ai-context" / "architecture_notes.md"
        if not notes_path.exists():
            notes_path = self.project_path / ".ai-context" / "project_brain.md"

        if notes_path.exists():
            try:
                return notes_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.warning(f"Could not read manual notes: {e}")
        return ""

    def _generate_outputs(self, results: Dict[str, Any], fmt: str):
        """Generate final report files based on analysis results."""
        try:
            ext = ".html" if fmt == "html" else ".md"
            reporting.generate_project_summary(
                results,
                self.project_path / f"PROJECT_SUMMARY{ext}",
                self.project_path.name,
                format=fmt,
            )
            reporting.generate_ai_context(
                results, self.project_path / "AI_CONTEXT.md", self.project_path.name
            )
            with open(
                self.project_path / "project_context.json", "w", encoding="utf-8"
            ) as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"Error generating outputs: {e}")
