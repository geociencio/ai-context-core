"""Reporting and context generation tools.

Generates executive Markdown summaries and optimized context files for
AI interaction (LLM prompts). Includes Mermaid graph support.
"""

import pathlib
import time
from typing import Any, Dict, Optional


def _short_name(path: str) -> str:
    """Derive a short, readable label from a relative file path.

    Args:
        path: Relative file path (e.g. ``core/logic.py``).

    Returns:
        A short node label without the ``.py`` suffix; ``__init__.py`` maps to
        its package directory name.
    """
    clean = path.replace("\\", "/")
    parts = [p for p in clean.split("/") if p]
    if not parts:
        return "root"
    name = parts[-1]
    if name.endswith(".py"):
        name = name[:-3]
    if name == "__init__":
        name = parts[-2] if len(parts) > 1 else "root"
    return name or "root"


def generate_dependency_diagram(dependencies: Dict[str, Any]) -> str:
    """Generates a Mermaid-formatted dependency graph for the top project modules."""
    import_graph = dependencies.get("import_graph", {})
    if not import_graph:
        return ""

    node_scores = {u: len(v) for u, v in import_graph.items()}
    top_nodes = sorted(node_scores.items(), key=lambda x: (-x[1], x[0]))[:20]
    top_node_names = {name for name, _ in top_nodes}

    ids: Dict[str, str] = {}
    used = set()

    def _node_id(path: str) -> str:
        if path in ids:
            return ids[path]
        base = _short_name(path)
        node_id = base
        counter = 0
        while node_id in used:
            counter += 1
            node_id = f"{base}_{counter}"
        ids[path] = node_id
        used.add(node_id)
        return node_id

    lines = ["graph TD"]
    cited = set()
    emitted = set()
    for u, neighbors in sorted(import_graph.items(), key=lambda kv: kv[0]):
        if u not in top_node_names and not any(v in top_node_names for v in neighbors):
            continue
        ul = _node_id(u)
        for v in sorted(neighbors):
            if u == v:
                continue
            vl = _node_id(v)
            if (ul, vl) in emitted:
                continue
            emitted.add((ul, vl))
            lines.append(f"    {ul} --> {vl}")
            cited.add(ul)
            cited.add(vl)

    lines.append("    classDef module fill:#f9f,stroke:#333,stroke-width:2px;")
    for node_id in sorted(cited):
        lines.append(f"    class {node_id} module;")

    return "\n".join(lines)


class MarkdownBuilder:
    """Helper class for building Markdown documents.

    Maintains a list of lines and provides methods to add sections and headers.
    """

    def __init__(self, title: str):
        """Initialize the builder with a document title.

        Args:
            title: The main title of the document.
        """
        from .. import __version__

        self.lines = [
            f"# {title}",
            f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Analyzer Version: {__version__} (Ai-Context-Core)",
            "",
        ]

    def add_section(self, title: str, content: str, level: int = 2):
        """Adds a section with a header and content.

        Args:
            title: Section title.
            content: Section markdown content.
            level: Markdown header level (1-6).
        """
        self.lines.append(f"{'#' * level} {title}")
        self.lines.append(content)
        self.lines.append("")

    def build(self) -> str:
        """Constructs the final Markdown document.

        Returns:
            The complete Markdown content as a string.
        """
        return "\n".join(self.lines)


def generate_project_summary(
    analyses: Dict[str, Any],
    output_path: pathlib.Path,
    project_name: str,
    format: str = "markdown",
) -> None:
    """Generates an executive summary of the project (markdown-only in v5.0.0).

    Args:
        analyses: Analysis results.
        output_path: Destination path.
        project_name: Project name used as the title.
        format: Retained for API compatibility; only markdown is produced.
    """
    from .summary_generator import ProjectSummaryGenerator

    gen = ProjectSummaryGenerator(analyses, project_name)
    gen.generate_markdown(output_path)


def generate_ai_context(
    analyses: Dict[str, Any],
    output_path: pathlib.Path,
    project_name: str,
    config: Optional[Dict[str, Any]] = None,
    max_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate ``AI_CONTEXT.md`` (optionally token-budgeted) and return a manifest.

    Args:
        analyses: Analysis results.
        output_path: Destination path for ``AI_CONTEXT.md``.
        project_name: Project name used as the title.
        config: Analyzer configuration (``context.sections`` / ``context.budget``).
        max_tokens: CLI override for the global token cap.

    Returns:
        A manifest with exact per-section token deltas, header tokens and total
        (``total == header + sum(sections)``), matching the rendered file.
    """
    from ...context.budget import budget_from_config
    from ...context.manifest import render_sections
    from .ai_context_generator import AIContextGenerator

    gen = AIContextGenerator(analyses, project_name, config=config)
    budget = budget_from_config(config, max_tokens=max_tokens)

    lines, manifest = render_sections(gen.header, gen.build_sections(), budget)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return manifest


def write_context_manifest(
    project_path: pathlib.Path,
    manifest: Dict[str, Any],
    provenance: Optional[Dict[str, Any]] = None,
) -> pathlib.Path:
    """Write ``context_manifest.json`` and return its path.

    Args:
        project_path: Project root.
        manifest: Token manifest returned by :func:`generate_ai_context`.
        provenance: Optional ``_meta`` block (source, tool_version, ...).

    Returns:
        The path of the written manifest.
    """
    import json

    payload = dict(manifest)
    if provenance:
        payload["_meta"] = provenance
    target = pathlib.Path(project_path) / "context_manifest.json"
    with open(target, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    return target
