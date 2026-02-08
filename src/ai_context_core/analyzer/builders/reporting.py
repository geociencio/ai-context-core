"""Reporting and context generation tools.

Generates executive Markdown summaries and optimized context files for
AI interaction (LLM prompts). Includes Mermaid graph support.
"""

import pathlib
import time
from typing import Dict, Any


def generate_dependency_diagram(dependencies: Dict[str, Any]) -> str:
    """Generates a Mermaid-formatted dependency graph for the top project modules."""
    graph = ["graph TD"]
    import_graph = dependencies.get("import_graph", {})
    if not import_graph:
        return ""

    node_scores = {u: len(v) for u, v in import_graph.items()}
    top_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)[:20]
    top_node_names = {name for name, _ in top_nodes}

    added_edges = set()
    for u, neighbors in import_graph.items():
        if u in top_node_names or any(v in top_node_names for v in neighbors):
            u_short = u.split("/")[-1].replace(".py", "").replace("__init__", "init")
            for v in neighbors:
                if u == v:
                    continue
                v_short = v.split(".")[-1]
                edge = f"{u_short}->{v_short}"
                if edge not in added_edges:
                    graph.append(f"    {u_short} --> {v_short}")
                    added_edges.add(edge)

    graph.append("    classDef module fill:#f9f,stroke:#333,stroke-width:2px;")
    for name in top_node_names:
        short = name.split("/")[-1].replace(".py", "").replace("__init__", "init")
        graph.append(f"    {short}")
        graph.append(f"    class {short} module;")

    return "\n".join(graph)


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
    """Generates an executive summary of the project."""
    from .summary_generator import ProjectSummaryGenerator

    gen = ProjectSummaryGenerator(analyses, project_name)
    if format == "html":
        gen.generate_html(output_path)
    else:
        gen.generate_markdown(output_path)


def generate_ai_context(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
) -> None:
    """Generates an optimized project overview file for AI consumption."""
    from .ai_context_generator import AIContextGenerator

    gen = AIContextGenerator(analyses, project_name)
    content = gen.build()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
