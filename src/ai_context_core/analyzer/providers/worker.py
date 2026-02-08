"""Module analysis workers and parallelization logic."""

import ast
import logging
import time
import concurrent.futures
import pathlib
from typing import Dict, Any, List
from ..visitors import ast_utils
from ..builders import calculator as metrics
from ..registry import registry
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
            cached = self.cache.get(rel)

            # Quick check: mtime and size
            stats = fs_utils.get_file_stats(f)
            if (
                cached
                and cached.get("mtime") == stats["mtime"]
                and cached.get("size") == stats["size"]
            ):
                # Most likely unchanged, trust the cache
                results.append(cached["data"])
                continue

            # Fallback to hash if mtime/size differ or not in cache
            h = fs_utils.calculate_file_hash(f)
            if cached and cached.get("hash") == h:
                # Content is same despite meta changes, update meta in cache but keep data
                cached["mtime"] = stats["mtime"]
                cached["size"] = stats["size"]
                results.append(cached["data"])
            else:
                to_analyze.append(f)

        if not to_analyze:
            return results

        if len(to_analyze) < PARALLEL_MIN_FILES:
            for f in to_analyze:
                self._analyze_and_cache(f, results)
            return results

        from ..constants import PARALLEL_BATCH_SIZE

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=self.max_workers
        ) as exc:
            batches = [
                to_analyze[i : i + PARALLEL_BATCH_SIZE]
                for i in range(0, len(to_analyze), PARALLEL_BATCH_SIZE)
            ]
            futures = {exc.submit(self.analyze_batch, b): b for b in batches}

            for fut in concurrent.futures.as_completed(futures):
                batch_files = futures[fut]
                try:
                    batch_results = fut.result()
                    for f, data in zip(batch_files, batch_results):
                        if data:
                            results.append(data)
                            self.cache[str(f.relative_to(self.project_path))] = {
                                "hash": fs_utils.calculate_file_hash(f),
                                "mtime": f.stat().st_mtime,
                                "size": f.stat().st_size,
                                "data": data,
                                "timestamp": time.time(),
                            }
                except Exception as e:
                    logger.error(f"Error analyzing batch {batch_files}: {e}")
                    for f in batch_files:
                        self.error_log[str(f)] = str(e)
        return results

    def analyze_batch(self, files: List[pathlib.Path]) -> List[Dict[str, Any]]:
        """Analyze a batch of files."""
        return [self.analyze_single(f) for f in files]

    def _analyze_and_cache(self, f: pathlib.Path, results: List[Dict[str, Any]]):
        from .. import fs_utils

        data = self.analyze_single(f)
        if data:
            results.append(data)
            self.cache[str(f.relative_to(self.project_path))] = {
                "hash": fs_utils.calculate_file_hash(f),
                "mtime": f.stat().st_mtime,
                "size": f.stat().st_size,
                "data": data,
                "timestamp": time.time(),
            }

    def analyze_single(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """Deep analysis of a single Python module."""
        from . import fs_utils

        # Ensure detectors are registered
        from ..visitors import antipatterns, issues, patterns, ast_qgis  # noqa: F401

        try:
            content = fs_utils.read_file_fast(file_path)
            if not content:
                return {}
            tree = ast.parse(content)

            entry_data = ast_utils.is_entry_point(tree)
            complexity = ast_utils.calculate_complexity(tree)
            halstead = ast_utils.calculate_halstead_metrics(tree)
            sloc = ast_utils.calculate_sloc(tree, content)

            res = {
                "path": str(file_path.relative_to(self.project_path)),
                "lines": len(content.splitlines()),
                "sloc": sloc,
                "loc": sloc,
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
                "maintenance_index": metrics.calculate_maintenance_index(
                    halstead["volume"], complexity, sloc
                ),
                "syntax_error": False,
            }

            # Inject dynamic detectors from registry
            for name, detector in registry.detectors.items():
                res[name] = detector(tree)

            return res
        except Exception as e:
            print(f"DEBUG: analyze_single FAILED for {file_path}: {e}")
            return {
                "path": str(file_path.relative_to(self.project_path)),
                "syntax_error": True,
                "error": str(e),
            }
