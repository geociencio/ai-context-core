"""Main orchestration engine for project analysis.

The ProjectAnalyzer coordinates the analysis of multiple Python modules,
aggregating results from AST analysis, dependency checking, and issue detection.
"""

import logging
import time
import pathlib
import json
from typing import Dict, Any, List, Optional
from .providers import (
    context_fields,
    fs_utils,
    git_analysis,
    worker,
)
from .builders import (
    reporting,
    aggregator,
    dependencies,
)
from ..context.manager import AIContextManager

logger = logging.getLogger(__name__)


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
        include_md: Optional[List[str]] = None,
    ):
        """Initialize the analyzer with project settings.

        Args:
            project_path: Absolute or relative path to the project root.
            config: Optional configuration dictionary.
            max_workers: Maximum number of parallel workers for analysis.
            exclude_patterns: List of glob patterns to exclude from scanning.
            ignore_cache: Whether to force a full analysis ignoring existing cache.
            include_md: Extra markdown globs (relative to the project root) to
                embed in the manual architecture notes.
        """
        from .providers.config_loader import load_config as loader_func

        self.project_path = pathlib.Path(project_path).resolve()
        self.max_workers = max_workers or (2 * (4 if hasattr(time, "get_clock_info") else 1))
        self.config = config or loader_func(self.project_path)

        self.exclusion_patterns = fs_utils.load_exclusion_patterns(
            self.project_path, exclude_patterns
        )
        self.include_md = list(include_md or [])
        self.context_manager = AIContextManager(project_path)
        self._config_fingerprint = fs_utils.compute_config_fingerprint(self.config)
        self.analysis_cache = (
            {} if ignore_cache else fs_utils.load_cache(self.project_path, self._config_fingerprint)
        )
        self.error_log = {}

    def collect(self) -> Dict[str, Any]:
        """Run the analysis pipeline and return results **without** rendering artifacts.

        This is the side-effect-free core consumed by the ``builtin`` analysis
        source; artifact rendering is handled by the source/render pipeline.

        Returns:
            A comprehensive dictionary containing all analysis results.
        """
        logger.info(f"Starting analysis for {self.project_path}")

        scan_res = fs_utils.scan_project(self.project_path, self.exclusion_patterns)
        analysis_worker = worker.AnalysisWorker(
            self.project_path, self.config, self.max_workers, self.analysis_cache
        )
        modules_data = analysis_worker.run_parallel(scan_res.python_files)
        self.error_log.update(analysis_worker.error_log)

        # 2. Dependency Analysis
        dep_analyzer = dependencies.DependencyAnalyzer(self.project_path)
        graph_data = dep_analyzer.build_graph(modules_data)

        # 3. Evolution analysis (Git)
        git_data = git_analysis.analyze_git_evolution(self.project_path, self.exclusion_patterns)

        # 4. Aggregate results
        qgis_metadata = fs_utils.parse_qgis_metadata(self.project_path)
        agg = aggregator.ResultsAggregator(self.project_path, self.config)
        results = agg.aggregate(modules_data, graph_data, git_data, qgis_metadata)

        # Add tree structure and manual notes
        results["structure"] = context_fields.build_structure(
            self.project_path, len(modules_data), scan_res=scan_res
        )
        results["manual_notes"] = context_fields.read_manual_notes(
            self.project_path, self.config, self.include_md
        )

        fs_utils.save_cache(self.project_path, self.analysis_cache, self._config_fingerprint)
        return results

    def analyze(
        self, output_format: str = "markdown", generate_summary: bool = True
    ) -> Dict[str, Any]:
        """Execute the project analysis pipeline and render the report artifacts.

        Orchestrates scanning, parallel module analysis, dependency graph building,
        git evolution tracking, and results aggregation.

        Args:
            output_format: Desired report format ('markdown' or 'html').
            generate_summary: When False, skip the score-focused
                ``PROJECT_SUMMARY`` output (context-only mode).

        Returns:
            A comprehensive dictionary containing all analysis results.
        """
        start_time = time.time()
        results = self.collect()
        self._generate_outputs(results, output_format, generate_summary)
        logger.info(f"Analysis completed in {time.time() - start_time:.2f}s")
        return results

    def _generate_outputs(self, results: Dict[str, Any], fmt: str, generate_summary: bool = True):
        """Generate final report files based on analysis results."""
        try:
            if generate_summary:
                ext = ".html" if fmt == "html" else ".md"
                reporting.generate_project_summary(
                    results,
                    self.project_path / f"PROJECT_SUMMARY{ext}",
                    self.project_path.name,
                    format=fmt,
                )
            reporting.generate_ai_context(
                results,
                self.project_path / "AI_CONTEXT.md",
                self.project_path.name,
                config=self.config,
            )
            with open(self.project_path / "project_context.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"Error generating outputs: {e}")
