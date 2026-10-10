"""Context compilation pipeline: source -> hybrid transform -> render.

The pipeline resolves an analysis source, optionally enriches its payload with
the *context-owned* sections (structure, git evolution, manual notes) that
``ai-context-core`` owns regardless of where the static analysis came from, and
renders the artifacts.
"""

import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

from ..analyzer.builders import reporting
from ..analyzer.providers import context_fields, fs_utils, git_analysis
from ..model import AnalysisResult
from .base import resolve_source

logger = logging.getLogger(__name__)


def enrich_context(
    data: Dict[str, Any],
    project_path: pathlib.Path,
    config: Dict[str, Any],
    include_md: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Fill context-owned sections missing from an analysis payload (hybrid).

    Only missing/empty sections are populated, so a builtin payload that already
    carries ``structure``/``git``/``manual_notes`` is returned unchanged.

    Args:
        data: Analysis payload to enrich in place.
        project_path: Project root.
        config: Analyzer configuration.
        include_md: Extra markdown globs to embed as manual notes.

    Returns:
        The enriched payload.
    """
    project_path = pathlib.Path(project_path).resolve()

    if not data.get("structure"):
        data["structure"] = context_fields.build_structure(
            project_path, len(data.get("modules") or [])
        )

    if not data.get("git"):
        patterns = fs_utils.load_exclusion_patterns(project_path, None)
        data["git"] = git_analysis.analyze_git_evolution(project_path, patterns)

    if "manual_notes" not in data:
        data["manual_notes"] = context_fields.read_manual_notes(project_path, config, include_md)

    _ensure_defaults(data)
    return data


def _ensure_defaults(data: Dict[str, Any]) -> None:
    """Guarantee the keys the context builders expect are present."""
    data.setdefault("project_name", "project")
    data.setdefault("metrics", {})
    data.setdefault("complexity", {})
    data.setdefault("modules", [])
    data.setdefault("dependencies", {})
    data.setdefault("entry_points", [])
    data.setdefault("security", [])
    data.setdefault("qgis_compliance", {})
    data.setdefault("optimizations", [])
    data.setdefault("recommendations", [])
    data.setdefault("patterns", {})
    data.setdefault("antipatterns", [])
    data.setdefault("git", {})
    data.setdefault("structure", {})
    data.setdefault("manual_notes", "")


def compile_context(
    project_path: pathlib.Path,
    config: Dict[str, Any],
    source: Optional[str] = "auto",
    *,
    max_workers: Optional[int] = None,
    ignore_cache: bool = False,
    include_md: Optional[List[str]] = None,
) -> AnalysisResult:
    """Resolve a source, collect its analysis, and apply the hybrid enrichment.

    Args:
        project_path: Project root.
        config: Analyzer configuration.
        source: ``auto`` | ``external`` | ``builtin``.
        max_workers: Parallel worker count (builtin only).
        ignore_cache: Force a full analysis (builtin only).
        include_md: Extra markdown globs to embed.

    Returns:
        The normalized, context-enriched analysis result.
    """
    provider = resolve_source(
        source,
        project_path,
        config,
        max_workers=max_workers,
        ignore_cache=ignore_cache,
        include_md=include_md,
    )
    result = provider.collect()
    enrich_context(result.data, project_path, config, include_md=include_md)
    return result


def render_context(
    result: AnalysisResult,
    project_path: pathlib.Path,
    config: Dict[str, Any],
    *,
    generate_summary: bool = False,
    output_format: str = "markdown",
) -> None:
    """Render the context artifacts for an analysis result.

    Args:
        result: The analysis result to render.
        project_path: Project root.
        config: Analyzer configuration (``context.sections``).
        generate_summary: Also emit ``PROJECT_SUMMARY`` (score-focused).
        output_format: ``markdown`` or ``html`` (affects the summary extension).
    """
    project_path = pathlib.Path(project_path).resolve()
    data = result.data

    if generate_summary:
        ext = ".html" if output_format == "html" else ".md"
        reporting.generate_project_summary(
            data,
            project_path / f"PROJECT_SUMMARY{ext}",
            project_path.name,
            format=output_format,
        )

    reporting.generate_ai_context(
        data,
        project_path / "AI_CONTEXT.md",
        project_path.name,
        config=config,
    )

    meta_payload = result.with_meta()
    with open(project_path / "project_context.json", "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, indent=2, ensure_ascii=False, default=str)
