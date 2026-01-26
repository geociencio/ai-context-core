"""Main orchestration engine for project analysis.

The ProjectAnalyzer coordinates the analysis of multiple Python modules,
aggregating results from AST analysis, dependency checking, and issue detection.
"""

import logging
import time
import ast
import concurrent.futures
import pathlib
import json
from typing import Dict, Any, List

from . import (
    ast_utils,
    fs_utils,
    metrics,
    issues,
    reporting,
    dependencies,
    antipatterns,
    patterns,
    git_analysis,
)
from ..context.manager import AIContextManager

logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    """Optimized and modular Python project analyzer.

    This class coordinates the analysis process, including file discovery,
    parallel module analysis, dependency graph construction, and report generation.

    Attributes:
        project_path: Absolute path to the project root.
        max_workers: Number of parallel workers for analysis.
        config: Configuration dictionary for metrics and thresholds.
        exclusion_patterns: List of patterns to exclude from analysis.
        context_manager: Manager for AI context files.
        ast_cache: Cache for parsed ASTs.
        file_cache: Cache for file contents.
        error_log: Log of errors encountered during analysis.
    """

    def __init__(
        self,
        project_path: str,
        config: Dict[str, Any] = None,
        max_workers: int = None,
        exclude_patterns: List[str] = None,
    ):
        """Initializes the ProjectAnalyzer.

        Args:
            project_path: Path to the project to analyze.
            config: Optional configuration dictionary.
            max_workers: Optional number of parallel workers.
            exclude_patterns: Optional list of exclusion patterns.
        """
        self.project_path = pathlib.Path(project_path).resolve()
        self.max_workers = max_workers or (
            2 * (1 if not hasattr(time, "get_clock_info") else 4)
        )  # Safe fallback
        self.config = config or {}

        # Load exclusion patterns
        self.exclusion_patterns = fs_utils.load_exclusion_patterns(
            self.project_path, exclude_patterns
        )

        # AI Context
        self.context_manager = AIContextManager(project_path)

        # Cache
        self.ast_cache = {}
        self.file_cache = {}

        # State
        self.error_log = {}

        # Default Config if not provided
        if not self.config:
            self._apply_default_config()

    def _apply_default_config(self):
        """Applies default configuration values for metrics and thresholds."""
        self.config = {
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

    def analyze(self) -> Dict[str, Any]:
        """Executes the complete project analysis pipeline.

        Returns:
            A dictionary containing aggregated analysis results, including metrics,
            structure, complexity distribution, dependencies, and issues.
        """
        start_time = time.time()
        logger.info(f"Starting analysis for {self.project_path}")

        # 1. Run Pipeline
        analysis_data = self._run_analysis_pipeline()

        # 2. Aggregate Results
        results = self._aggregate_results(analysis_data)

        # 3. Generate Outputs
        self._generate_outputs(results)

        logger.info(f"Analysis completed in {time.time() - start_time:.2f}s")
        return results

    def _run_analysis_pipeline(self) -> Dict[str, Any]:
        """Runs the sequential analysis steps in the pipeline.

        Returns:
            A dictionary with intermediate analysis data (modules, deps, structure).
        """
        # 1. Get files
        python_files = fs_utils.get_python_files_filtered(
            self.project_path, self.exclusion_patterns
        )
        logger.info(f"Found {len(python_files)} Python files")

        # 2. Parallel module analysis
        modules_data = self._analyze_modules_parallel(python_files)

        # 3. Dependencies
        deps_data = dependencies.analyze_dependencies(
            modules_data, self.project_path, fs_utils.read_file_fast
        )

        # 4. Structure and Tests
        structure = fs_utils.analyze_structure(self.project_path, len(modules_data))
        test_files_count = fs_utils.count_test_files(self.project_path, self.exclusion_patterns)

        # 5. Git Analysis
        git_data = {
            "hotspots": git_analysis.get_git_hotspots(self.project_path),
            "churn": git_analysis.get_git_churn(self.project_path),
        }

        return {
            "modules_data": modules_data,
            "deps_data": deps_data,
            "structure": structure,
            "test_files_count": test_files_count,
            "git_data": git_data,
        }

    def _aggregate_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregates raw analysis data into a structured result dictionary.

        Args:
            data: The intermediate data from the analysis pipeline.

        Returns:
            The finalized results dictionary with derived metrics and sorted issues.
        """
        modules_data = data["modules_data"]
        deps_data = data["deps_data"]
        structure = data["structure"]
        test_files_count = data["test_files_count"]
        git_data = data.get("git_data", {})

        entry_points = [m["path"] for m in modules_data if m.get("has_main")]

        # Project metrics
        project_metrics = metrics.calculate_project_metrics(
            modules_data,
            entry_points,
            test_files_count,
            self.config,
            {"qgis_compliance": {}},  # TODO: Implement real QGIS compliance
        )

        complexity_dist = metrics.calculate_complexity_distribution(modules_data)

        # Debt and suggestions
        tech_debt = issues.find_technical_debt(modules_data)
        optimization_suggestions = issues.find_optimizations(modules_data)
        security_list = issues.find_security_issues(modules_data, str(self.project_path))

        # Merge AST security
        for m in modules_data:
            if m.get("ast_security"):
                items = m["ast_security"]
                existing = next((x for x in security_list if x["module"] == m["path"]), None)
                if existing:
                    existing["issues"].extend(items)
                    existing["total_issues"] += len(items)
                    # Simple severity update: if any new issue is high, upgrade existing
                    current_max = existing["max_severity"]
                    new_max = max(
                        (i["severity"] for i in items),
                        key=lambda x: {"high": 3, "medium": 2, "low": 1}[x],
                    )
                    if {"high": 3, "medium": 2, "low": 1}[new_max] > {
                        "high": 3,
                        "medium": 2,
                        "low": 1,
                    }[current_max]:
                        existing["max_severity"] = new_max
                else:
                    security_list.append(
                        {
                            "module": m["path"],
                            "issues": items,
                            "total_issues": len(items),
                            "max_severity": max(
                                (i["severity"] for i in items),
                                key=lambda x: {"high": 3, "medium": 2, "low": 1}[x],
                            ),
                        }
                    )

        # Aggregate antipatterns
        antipatterns_list = []
        for m in modules_data:
            if m.get("antipatterns"):
                antipatterns_list.append(
                    {
                        "module": m["path"],
                        "issues": m["antipatterns"],
                        "total_issues": len(m["antipatterns"]),
                    }
                )

        return {
            "project_name": self.project_path.name,
            "timestamp": time.time(),
            "metrics": project_metrics,
            "structure": structure,
            "complexity": {
                "total_modules": len(modules_data),
                "total_lines": project_metrics.get("total_lines_code", 0),
                "total_functions": sum(len(m.get("functions", [])) for m in modules_data),
                "total_classes": sum(len(m.get("classes", [])) for m in modules_data),
                "average_complexity": project_metrics.get("avg_complexity", 0),
                "complexity_distribution": complexity_dist,
                "most_complex_modules": sorted(
                    [(m["path"], m["complexity"]) for m in modules_data],
                    key=lambda x: x[1],
                    reverse=True,
                )[:5],
            },
            "dependencies": deps_data,
            "debt": tech_debt,
            "optimizations": optimization_suggestions,
            "security": security_list,
            "antipatterns": antipatterns_list,
            "entry_points": entry_points,
            "patterns": self._aggregate_patterns(modules_data),
            "git": git_data,
        }

    def _aggregate_patterns(self, modules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates detected design patterns from all modules.

        Args:
            modules_data: List of analyzed module data.

        Returns:
            A dictionary of patterns grouped by type.
        """
        aggregated = {}
        for m in modules_data:
            module_patterns = m.get("patterns", {})
            for pattern_name, results in module_patterns.items():
                if pattern_name not in aggregated:
                    aggregated[pattern_name] = []

                # 'results' is a list of occurrences (e.g., list of singletons in this module)
                for res in results:
                    res["module"] = m["path"]
                    aggregated[pattern_name].append(res)

        return aggregated

    def _generate_outputs(self, results: Dict[str, Any]):
        """Generates markdown reports and JSON context files from the results.

        Args:
            results: The aggregated analysis results.
        """
        try:
            reporting.generate_project_summary(
                results,
                self.project_path / "PROJECT_SUMMARY.md",
                self.project_path.name,
            )
            reporting.generate_ai_context(
                results, self.project_path / "AI_CONTEXT.md", self.project_path.name
            )

            # Save full JSON
            with open(self.project_path / "project_context.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            logger.error(f"Error generating outputs: {e}")

    def _analyze_modules_parallel(self, files: List[pathlib.Path]) -> List[Dict[str, Any]]:
        """Analyzes multiple modules in parallel using a process pool.

        Args:
            files: List of Python file paths to analyze.

        Returns:
            A list of dictionaries, one per successfully analyzed module.
        """
        results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self._analyze_single_module, f): f for f in files}

            for future in concurrent.futures.as_completed(future_to_file):
                f = future_to_file[future]
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception as e:
                    logger.error(f"Error analyzing {f}: {e}")
                    self.error_log[str(f)] = str(e)

        return results

    def _analyze_single_module(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """Parses and calculates metrics for a single Python module.

        Args:
            file_path: Path to the Python file.

        Returns:
            A dictionary containing module metrics (complexity, imports, functions, etc.).
        """
        try:
            content = fs_utils.read_file_fast(file_path)
            if not content:
                return {}

            tree = ast.parse(content)
            entry_point_data = ast_utils.is_entry_point(tree)

            # Detect antipatterns
            detected_antipatterns = []
            detected_antipatterns.extend(antipatterns.detect_god_object(tree))
            detected_antipatterns.extend(antipatterns.detect_spaghetti_code(tree))
            detected_antipatterns.extend(antipatterns.detect_magic_numbers(tree))
            detected_antipatterns.extend(antipatterns.detect_dead_code(tree))

            ast_security = issues.detect_ast_security_issues(tree)

            return {
                "path": str(file_path.relative_to(self.project_path)),
                "lines": len(content.splitlines()),
                "file_size_kb": file_path.stat().st_size / 1024,
                "complexity": ast_utils.calculate_complexity(tree),
                "imports": ast_utils.extract_imports(tree),
                "classes": ast_utils.extract_classes(tree),
                "functions": ast_utils.extract_functions(tree),
                "docstrings": ast_utils.check_docstrings(tree),
                "entry_point_info": entry_point_data,
                "has_main": entry_point_data["is_entry_point"],
                "type_hints": ast_utils.calculate_type_hint_coverage(tree),
                "halstead": ast_utils.calculate_halstead_metrics(tree),
                "antipatterns": detected_antipatterns,
                "ast_security": ast_security,
                "patterns": patterns.detect_patterns(tree),
                "unused_imports": ast_utils.detect_unused_imports(tree),
                "maintenance_index": metrics.calculate_maintenance_index(
                    ast_utils.calculate_halstead_metrics(tree)["volume"],
                    ast_utils.calculate_complexity(tree),
                    len(content.splitlines()),
                ),
                "syntax_error": False,
            }

        except SyntaxError:
            return {
                "path": str(file_path.relative_to(self.project_path)),
                "syntax_error": True,
                "error": "SyntaxError",
            }
        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.project_path)),
                "syntax_error": True,
                "error": str(e),
            }
