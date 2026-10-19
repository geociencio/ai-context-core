"""Regression tests for reproducible (deterministic) context artifacts."""

import concurrent.futures
import pathlib
from typing import List

from ai_context_core.analyzer.providers import worker
from ai_context_core.sources.pipeline import compile_context, render_context


def _write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _fixture(root: pathlib.Path, modules: int = 6) -> List[pathlib.Path]:
    files = []
    for index in range(modules):
        path = root / "pkg" / f"mod_{index:02d}.py"
        _write(path, f"def f_{index}():\n    return {index}\n")
        files.append(path)
    _write(root / "pkg" / "__init__.py", "")
    return files


class _ImmediateExecutor:
    """Executor whose futures resolve immediately, in submitted batch order."""

    def __init__(self, *args, **kwargs):
        self.created = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def submit(self, _fn, batch):
        future: concurrent.futures.Future = concurrent.futures.Future()
        future.set_result([{"path": str(path)} for path in batch])
        self.created.append(future)
        return future


def test_worker_sorts_parallel_results(monkeypatch, tmp_path):
    from ai_context_core.analyzer import constants

    files = _fixture(tmp_path)
    analysis_worker = worker.AnalysisWorker(tmp_path, {}, max_workers=1, cache={})
    monkeypatch.setattr(analysis_worker, "_partition_by_cache", lambda _files: ([], list(_files)))
    monkeypatch.setattr(concurrent.futures, "ProcessPoolExecutor", _ImmediateExecutor)
    monkeypatch.setattr(
        concurrent.futures,
        "as_completed",
        lambda futures: reversed(list(futures)),
    )
    monkeypatch.setattr(constants, "PARALLEL_BATCH_SIZE", 1)

    results = analysis_worker.run_parallel(files)

    paths = [result["path"] for result in results]
    assert paths == sorted(paths)


def test_aggregator_sorts_modules(tmp_path):
    from ai_context_core.analyzer.builders.aggregator import ResultsAggregator

    modules = [
        {"path": name, "complexity": 1, "lines": 1, "sloc": 1} for name in ("c.py", "a.py", "b.py")
    ]
    aggregated = ResultsAggregator(tmp_path, {}).aggregate(modules, {}, {}, {})

    assert [module["path"] for module in aggregated["modules"]] == [
        "a.py",
        "b.py",
        "c.py",
    ]


def test_context_render_is_byte_stable(tmp_path):
    _fixture(tmp_path)
    config = {"context": {"sections": ["structure", "metrics", "dependencies", "git"]}}

    # Pre-create the artifacts: the structure tree lists root files, so the
    # first and second renders must observe the same filesystem.
    for name in (
        "AI_CONTEXT.md",
        "project_context.json",
        "context_manifest.json",
        ".ai_context_cache.json",
    ):
        _write(tmp_path / name, "")

    first_result = compile_context(tmp_path, config, "builtin", max_workers=2, ignore_cache=True)
    render_context(first_result, tmp_path, config)
    first = (tmp_path / "AI_CONTEXT.md").read_bytes()
    first_order = [module["path"] for module in first_result.data["modules"]]

    second_result = compile_context(tmp_path, config, "builtin", max_workers=2, ignore_cache=True)
    render_context(second_result, tmp_path, config)
    second = (tmp_path / "AI_CONTEXT.md").read_bytes()
    second_order = [module["path"] for module in second_result.data["modules"]]

    assert first_order == sorted(first_order)
    assert first_order == second_order
    assert first == second
