"""Context-owned fields shared by the engine and the source pipeline.

The structure tree, manual architecture notes and git evolution are *context*
concerns owned by ``ai-context-core`` (not by an external analysis source). They
are centralized here so both the builtin engine and the hybrid source pipeline
produce identical sections.
"""

import logging
import pathlib
from typing import Any, Dict, List, Optional

from . import fs_utils
from .fs_scanner import ProjectScanResult

logger = logging.getLogger(__name__)

_BASE_NOTE_NAMES = ("architecture_notes.md", "project_brain.md")


def build_structure(
    project_path: pathlib.Path,
    modules_count: int,
    scan_res: Optional[ProjectScanResult] = None,
    exclusion_patterns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build the ``structure`` section (tree plus scan statistics).

    Args:
        project_path: Project root.
        modules_count: Number of analyzed modules.
        scan_res: Optional pre-computed scan result to avoid a second scan.
        exclusion_patterns: Patterns used when ``scan_res`` is ``None``.

    Returns:
        The structure dictionary consumed by ``StructureBuilder``.
    """
    if scan_res is None:
        scan_res = fs_utils.scan_project(project_path, exclusion_patterns or [])
    return {
        "tree": fs_utils.generate_tree_optimized(project_path),
        "modules_count": modules_count,
        "file_types": scan_res.file_types,
        "size_stats": scan_res.size_stats,
    }


def read_manual_notes(
    project_path: pathlib.Path,
    config: Dict[str, Any],
    include_md: Optional[List[str]] = None,
) -> str:
    """Read base architecture notes plus configured extra context docs.

    Args:
        project_path: Project root.
        config: Analyzer configuration (``context_docs`` globs).
        include_md: Extra markdown globs (relative to the root) to embed.

    Returns:
        Concatenated markdown with the base notes first, followed by each extra
        document under its own ``### <relative-path>`` heading.
    """
    sections: List[str] = []

    base_notes = _read_base_notes(project_path)
    if base_notes:
        sections.append(base_notes)

    for doc in _discover_context_docs(project_path, config, include_md):
        rel = doc.relative_to(project_path)
        try:
            content = doc.read_text(encoding="utf-8", errors="replace").strip()
        except OSError as e:
            logger.warning("Could not read context doc %s: %s", rel, e)
            continue
        if content:
            sections.append(f"### {rel}\n\n{content}")

    return "\n\n".join(sections)


def _read_base_notes(project_path: pathlib.Path) -> str:
    """Read the conventional architecture notes file if present."""
    for name in _BASE_NOTE_NAMES:
        notes_path = project_path / ".ai-context" / name
        if notes_path.exists():
            try:
                return notes_path.read_text(encoding="utf-8")
            except OSError as e:
                logger.warning("Could not read manual notes: %s", e)
    return ""


def _discover_context_docs(
    project_path: pathlib.Path,
    config: Dict[str, Any],
    include_md: Optional[List[str]],
) -> List[pathlib.Path]:
    """Resolve config ``context_docs`` and CLI ``include_md`` globs.

    Returns:
        Sorted, de-duplicated list of matching files.
    """
    patterns: List[str] = list(config.get("context_docs", []) or [])
    patterns.extend(include_md or [])

    docs: List[pathlib.Path] = []
    seen = set()
    for pattern in patterns:
        for path in sorted(project_path.glob(pattern)):
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            docs.append(path)
    return docs
