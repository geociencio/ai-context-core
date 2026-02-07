"""Module analysis workers and parallelization logic."""

import ast
import logging
import time
import concurrent.futures
import pathlib
from typing import Dict, Any, List
from .. import ast_utils, issues, patterns, metrics
from ..constants import PARALLEL_MIN_FILES

logger = logging.getLogger(__name__)


class AnalysisWorker:
    """Handles individual and parallel module analysis."""

    def __init__(
        self,
        project_path: pathlib.Path,
        config: Dict[str, Any],
        max_workers: int,
        cache: Dict[str, Any],
    ):
        self.project_path = project_path
        self.config = config
        self.max_workers = max_workers
        self.cache = cache
        self.error_log = {}

    def run_parallel(self, files: List[pathlib.Path]) -> List[Dict[str, Any]]:
        """Executes parallel analysis of modules."""
        results, to_analyze = [], []
        from .. import fs_utils

        # DEBUG:
        # print(f"run_parallel called with {len(files)} files")
        for f in files:
            rel = str(f.relative_to(self.project_path))
            h = fs_utils.calculate_file_hash(f)
            cached = self.cache.get(rel)
            if cached and cached.get("hash") == h:
                results.append(cached["data"])
            else:
                to_analyze.append(f)

        if not to_analyze:
            return results

        if len(to_analyze) < PARALLEL_MIN_FILES:
            for f in to_analyze:
                self._analyze_and_cache(f, results)
            return results

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=self.max_workers
        ) as exc:
            futures = {exc.submit(self.analyze_single, f): f for f in to_analyze}
            for fut in concurrent.futures.as_completed(futures):
                f = futures[fut]
                try:
                    data = fut.result()
                    if data:
                        results.append(data)
                        self.cache[str(f.relative_to(self.project_path))] = {
                            "hash": fs_utils.calculate_file_hash(f),
                            "data": data,
                            "timestamp": time.time(),
                        }
                except Exception as e:
                    logger.error(f"Error analyzing {f}: {e}")
                    self.error_log[str(f)] = str(e)
        return results

    def _analyze_and_cache(self, f: pathlib.Path, results: List[Dict[str, Any]]):
        from .. import fs_utils

        data = self.analyze_single(f)
        if data:
            results.append(data)
            self.cache[str(f.relative_to(self.project_path))] = {
                "hash": fs_utils.calculate_file_hash(f),
                "data": data,
                "timestamp": time.time(),
            }

    def analyze_single(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """Deep analysis of a single Python module."""
        from .. import fs_utils, antipattern_orchestrator

        try:
            content = fs_utils.read_file_fast(file_path)
            if not content:
                return {}
            tree = ast.parse(content)

            entry_data = ast_utils.is_entry_point(tree)
            complexity = ast_utils.calculate_complexity(tree)
            halstead = ast_utils.calculate_halstead_metrics(tree)
            sloc = ast_utils.calculate_sloc(tree, content)

            return {
                "path": str(file_path.relative_to(self.project_path)),
                "lines": len(content.splitlines()),
                "sloc": sloc,
                "file_size_kb": file_path.stat().st_size / 1024,
                "complexity": complexity,
                "imports": ast_utils.extract_imports(tree),
                "classes": ast_utils.extract_classes(tree),
                "functions": ast_utils.extract_functions(tree),
                "docstrings": ast_utils.check_docstrings(tree),
                "entry_point_info": entry_data,
                "has_main": entry_data["is_entry_point"],
                "type_hints": ast_utils.calculate_type_hint_coverage(tree),
                "halstead": halstead,
                "antipatterns": antipattern_orchestrator.detect_all(tree),
                "ast_security": issues.detect(tree),
                "patterns": patterns.detect_patterns(tree),
                "unused_imports": ast_utils.detect_unused_imports(tree),
                "maintenance_index": metrics.calculate_maintenance_index(
                    halstead["volume"], complexity, sloc
                ),
                "qgis_compliance": ast_utils.check_qgis_compliance(tree),
                "syntax_error": False,
            }
        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.project_path)),
                "syntax_error": True,
                "error": str(e),
            }
