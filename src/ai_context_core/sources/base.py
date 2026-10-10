"""Analysis source protocol and resolution.

The extraction layer of the context compiler is pluggable: a source produces a
normalized :class:`~ai_context_core.model.AnalysisResult` that the transform and
render layers consume. Two sources ship today:

* ``builtin`` — the internal AST engine (``ProjectAnalyzer``).
* ``external`` — reads ``qgis-plugin-analyzer`` output from
  ``analysis_results/project_context.json``.
"""

import logging
import pathlib
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from ..analyzer.providers.runner import GitRunner
from ..model import AnalysisResult

logger = logging.getLogger(__name__)

VALID_SOURCES = ("auto", "external", "builtin")
EXTERNAL_DEFAULT_PATH = pathlib.Path("analysis_results") / "project_context.json"


@runtime_checkable
class AnalysisProvider(Protocol):
    """Extraction-layer contract: produce a normalized analysis result."""

    name: str

    def collect(self) -> AnalysisResult:
        """Return the normalized analysis payload."""
        ...


def current_git_sha(project_path: pathlib.Path) -> Optional[str]:
    """Return the current git revision of a project, or ``None`` when unavailable."""
    out = GitRunner(pathlib.Path(project_path)).run(["rev-parse", "HEAD"], check=False)
    return out.strip() if out else None


def external_output_path(
    project_path: pathlib.Path, config: Optional[Dict[str, Any]] = None
) -> Optional[pathlib.Path]:
    """Return the external analyzer output path when it exists.

    Args:
        project_path: Project root.
        config: Analyzer configuration; ``[sources].external_path`` overrides the
            default ``analysis_results/project_context.json``.

    Returns:
        The first existing candidate path, or ``None``.
    """
    cfg = config or {}
    override = (cfg.get("sources") or {}).get("external_path")
    candidates: List[pathlib.Path] = []
    if override:
        candidates.append(project_path / override)
    candidates.append(project_path / EXTERNAL_DEFAULT_PATH)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def requested_source(source: Optional[str], config: Dict[str, Any]) -> str:
    """Resolve the requested source, falling back to ``[sources].source``."""
    if source and source != "auto":
        return source
    configured = (config.get("sources") or {}).get("source")
    if not configured:
        return "auto"
    return configured


def resolve_source(
    source: Optional[str],
    project_path: pathlib.Path,
    config: Dict[str, Any],
    *,
    max_workers: Optional[int] = None,
    ignore_cache: bool = False,
    include_md: Optional[List[str]] = None,
) -> AnalysisProvider:
    """Resolve and construct the analysis source to use.

    Args:
        source: ``auto`` | ``external`` | ``builtin`` (``None`` defers to config).
        project_path: Project root.
        config: Analyzer configuration.
        max_workers: Parallel worker count (builtin only).
        ignore_cache: Force a full analysis (builtin only).
        include_md: Extra markdown globs to embed (builtin only).

    Returns:
        A concrete :class:`AnalysisProvider`.

    Raises:
        ValueError: If the requested source name is not recognized.
    """
    requested = requested_source(source, config)
    if requested not in VALID_SOURCES:
        raise ValueError(
            f"Unknown source {requested!r}; expected one of {', '.join(VALID_SOURCES)}."
        )

    resolved = requested
    if resolved == "auto":
        resolved = (
            "external" if external_output_path(project_path, config) is not None else "builtin"
        )

    if resolved == "external":
        from .external.qgis_analyzer import ExternalSource

        return ExternalSource(project_path, config)

    from .builtin.engine_source import BuiltinSource

    return BuiltinSource(
        project_path,
        config,
        max_workers=max_workers,
        ignore_cache=ignore_cache,
        include_md=include_md,
    )
