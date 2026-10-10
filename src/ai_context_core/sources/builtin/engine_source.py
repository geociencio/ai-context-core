"""Builtin analysis source backed by the internal AST engine."""

import pathlib
from typing import Any, Dict, List, Optional

from ... import __version__
from ...analyzer.engine import ProjectAnalyzer
from ...model import SCHEMA_VERSION, AnalysisResult, Provenance
from ..base import current_git_sha


class BuiltinSource:
    """Produce analysis results with the internal ``ProjectAnalyzer``.

    The engine runs its full AST pipeline but does **not** render artifacts;
    rendering is the responsibility of the source/render pipeline.
    """

    name = "builtin"

    def __init__(
        self,
        project_path: pathlib.Path,
        config: Dict[str, Any],
        max_workers: Optional[int] = None,
        ignore_cache: bool = False,
        include_md: Optional[List[str]] = None,
    ):
        """Initialize the builtin source.

        Args:
            project_path: Project root.
            config: Analyzer configuration.
            max_workers: Parallel worker count.
            ignore_cache: Force a full analysis ignoring the cache.
            include_md: Extra markdown globs to embed as manual notes.
        """
        self.project_path = pathlib.Path(project_path).resolve()
        self.config = config
        self.max_workers = max_workers
        self.ignore_cache = ignore_cache
        self.include_md = include_md

    def collect(self) -> AnalysisResult:
        """Run the internal engine and wrap the results with provenance."""
        analyzer = ProjectAnalyzer(
            project_path=str(self.project_path),
            config=self.config,
            max_workers=self.max_workers,
            ignore_cache=self.ignore_cache,
            include_md=self.include_md,
        )
        data = analyzer.collect()
        return AnalysisResult(
            data=data,
            provenance=Provenance(
                source=self.name,
                schema=SCHEMA_VERSION,
                tool_version=__version__,
                git_sha=current_git_sha(self.project_path),
            ),
        )
