"""Reporting and context generation tools.

Generates executive Markdown summaries and optimized context files for
AI interaction (LLM prompts). Includes Mermaid graph support.
"""

import pathlib
import time
from typing import Dict, Any


import string


def generate_dependency_diagram(dependencies: Dict[str, Any]) -> str:
    """Generates a Mermaid-formatted dependency graph for the top project modules.

    Args:
        dependencies: Dependency analysis dictionary containing import graphs.

    Returns:
        A string representing the Mermaid dependency graph.
    """
    graph = ["graph TD"]
    import_graph = dependencies.get("import_graph", {})
    if not import_graph:
        return ""

    # Calculate node scores (connections) to filter noisy graphs
    node_scores = {u: len(v) for u, v in import_graph.items()}
    # Filter out likely external packages if any slipped through or low-value nodes
    top_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)[:20]
    top_node_names = {name for name, _ in top_nodes}

    # Add edges
    added_edges = set()
    for u, neighbors in import_graph.items():
        if u in top_node_names or any(v in top_node_names for v in neighbors):
            u_short = u.split("/")[-1].replace(".py", "").replace("__init__", "init")
            for v in neighbors:
                # Filter self-loops and internal implementation details if needed
                if u == v:
                    continue

                v_short = v.split(".")[-1]
                edge = f"{u_short}->{v_short}"

                if edge not in added_edges:
                    graph.append(f"    {u_short} --> {v_short}")
                    added_edges.add(edge)

    # Styling
    graph.append("    classDef module fill:#f9f,stroke:#333,stroke-width:2px;")
    # Apply class to top nodes and ensure they are rendered
    for name in top_node_names:
        short = name.split("/")[-1].replace(".py", "").replace("__init__", "init")
        graph.append(f"    {short}")  # Explicitly declare node
        graph.append(f"    class {short} module;")

    return "\n".join(graph)


generate_mermaid_graph = (
    generate_dependency_diagram  # Alias for backward compatibility if needed
)


class MarkdownBuilder:
    """Helper class for building Markdown documents."""

    def __init__(self, title: str):
        self.lines = [
            f"# {title}",
            f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "Analyzer Version: 2.0 (Ai-Context-Core)",
            "",
        ]

    def add_section(self, title: str, level: int = 2):
        """Adds a section header."""
        self.lines.append(f"{'#' * level} {title}")

    def add_text(self, text: str):
        """Adds raw text or formatted blocks."""
        self.lines.append(text)

    def add_list_item(self, text: str, bullet: str = "-"):
        """Adds a bulleted list item."""
        self.lines.append(f"{bullet} {text}")

    def add_list(self, items: list, bullet: str = "-"):
        """Adds multiple list items."""
        for item in items:
            self.add_list_item(item, bullet)

    def build(self) -> str:
        """Returns the complete Markdown string."""
        return "\n".join(self.lines)


class HTMLBuilder:
    """Helper class for building HTML documents using string.Template."""

    CSS = """
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background: #f4f6f9; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2 { color: #2c3e50; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }
    h3 { color: #34495e; }
    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .metric { display: inline-block; margin-right: 20px; font-weight: bold; }
    .metric-value { color: #2980b9; }
    ul { list-style-type: none; padding: 0; }
    li { padding: 5px 0; border-bottom: 1px solid #eee; }
    li:last-child { border-bottom: none; }
    .badge { padding: 3px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; color: white; display: inline-block; }
    .badge-critical { background: #e74c3c; }
    .badge-high { background: #e67e22; }
    .badge-medium { background: #f1c40f; color: #333; }
    .badge-low { background: #3498db; }
    .mermaid { text-align: center; overflow-x: auto; background: white; padding: 20px; }
    """

    TEMPLATE = string.Template(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title</title>
    <style>$css</style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
</head>
<body>
    <h1>$title</h1>
    <div class="card">
        <p><strong>Date:</strong> $date</p>
        <p><strong>Version:</strong> 2.0 (Ai-Context-Core)</p>
    </div>
    $content
</body>
</html>
    """
    )

    def __init__(self, title: str):
        self.title = title
        self.content_parts = []

    def add_section(self, title: str, content: str):
        """Adds a section wrapped in a card."""
        self.content_parts.append(f'<div class="card"><h2>{title}</h2>{content}</div>')

    def add_raw(self, html: str):
        """Adds raw HTML."""
        self.content_parts.append(html)

    def build_list(self, items: list) -> str:
        """Helper to build an HTML list."""
        if not items:
            return ""
        lis = "".join(f"<li>{item}</li>" for item in items)
        return f"<ul>{lis}</ul>"

    def render(self) -> str:
        """Renders final HTML."""
        return self.TEMPLATE.substitute(
            title=self.title,
            css=self.CSS,
            date=time.strftime("%Y-%m-%d %H:%M:%S"),
            content="\n".join(self.content_parts),
        )


def generate_project_summary(
    analyses: Dict[str, Any],
    output_path: pathlib.Path,
    project_name: str,
    format: str = "markdown",
) -> None:
    """Generates an executive summary of the project.

    Args:
        analyses: Aggregated analysis results dictionary.
        output_path: File system path to write the report to.
        project_name: Human-readable name of the project.
        format: 'markdown' or 'html'.
    """
    if format == "html":
        _generate_project_summary_html(analyses, output_path, project_name)
    else:
        _generate_project_summary_md(analyses, output_path, project_name)


def _generate_project_summary_html(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
):
    builder = HTMLBuilder(f"PROJECT SUMMARY - {project_name}")

    # Key Metrics
    metrics = analyses.get("metrics", {})
    m_html = f"""
    <div class="metric">Quality Score: <span class="metric-value">{metrics.get("quality_score", 0)}/100</span></div>
    <div class="metric">Lines of Code: <span class="metric-value">{metrics.get('total_lines_code', 0):,}</span></div>
    <div class="metric">Modules: <span class="metric-value">{analyses.get('complexity', {}).get('total_modules', 0)}</span></div>
    """
    builder.add_section("📊 KEY METRICS", m_html)

    # Issues
    security = analyses.get("security", [])
    if security:
        sec_list = [
            f"<strong>{i['module']}</strong>: {i['total_issues']} issues (Max: {i['max_severity']})"
            for i in security[:5]
        ]
        builder.add_section("🚨 SECURITY ISSUES", builder.build_list(sec_list))

    # Optimizations
    opt = analyses.get("optimizations", [])
    if opt:
        opt_list = []
        for o in opt[:5]:
            msgs = [s.get("message", "") for s in o.get("suggestions", [])]
            opt_list.append(f"<strong>{o.get('module')}</strong>: {'; '.join(msgs)}")
        builder.add_section("💡 RECOMMENDATIONS", builder.build_list(opt_list))

    # Dependency Graph
    graph = generate_dependency_diagram(analyses.get("dependencies", {}))
    if graph:
        builder.add_section("🕸️ DEPENDENCY GRAPH", f'<div class="mermaid">{graph}</div>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(builder.render())


def _generate_project_summary_md(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
) -> None:
    """Generates the Markdown summary (original implementation)."""
    builder = MarkdownBuilder(f"PROJECT SUMMARY - {project_name}")

    builder.add_text(_build_key_metrics_section(analyses))
    builder.add_text(_build_structure_section(analyses))
    builder.add_text(_build_critical_issues_section(analyses))
    builder.add_text(_build_qgis_compliance_section(analyses))
    builder.add_text(_build_recommendations_section(analyses))
    builder.add_text(_build_patterns_summary_section(analyses))
    builder.add_text(_build_git_analysis_section(analyses))
    builder.add_text(_build_complexity_dist_section(analyses))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(builder.build())


def _build_key_metrics_section(analyses: Dict[str, Any]) -> str:
    """Builds the formatted Key Metrics section of the summary."""
    complexity = analyses.get("complexity", {})
    metrics = analyses.get("metrics", {})
    structure = analyses.get("structure", {})
    size_stats = structure.get("size_stats", {})

    return f"""## 📊 KEY METRICS
- **Total Modules**: {complexity.get("total_modules", 0):,}
- **Lines of Code**: {complexity.get("total_lines", 0):,}
- **Total Size**: {size_stats.get("total_size_mb", 0):.1f} MB
- **Average Complexity**: {complexity.get("average_complexity", 0):.1f}
- **Avg Maintenance Index**: {metrics.get("avg_maintenance_index", 0):.1f}
- **Docstring Coverage**: {metrics.get("docstring_coverage", 0):.1f}%
- **Quality Score**: {metrics.get("quality_score", 0):.1f}/100
- **Test Files**: {metrics.get("test_files_count", 0)}"""


def _build_structure_section(analyses: Dict[str, Any]) -> str:
    """Builds the project structure overview section."""
    structure = analyses.get("structure", {})
    size_stats = structure.get("size_stats", {})
    file_types = list(structure.get("file_types", {}).keys())

    return f"""
## 📁 STRUCTURE
- **Python Files**: {size_stats.get("python_files", 0)}
- **Total Files**: {size_stats.get("total_files", 0)}
- **Primary File Types**: {", ".join(file_types[:5])}"""


def _build_critical_issues_section(analyses: Dict[str, Any]) -> str:
    """Compiles the Critical Issues section, including security and technical debt."""
    lines = ["\n## 🚨 CRITICAL ISSUES"]

    # Security
    security = analyses.get("security", [])
    if security:
        lines.append("\n### 🔒 Security Issues:")
        for item in security[:3]:
            lines.append(
                f"- **{item['module']}**: {item['total_issues']} issues (Max: {item['max_severity'].upper()})"
            )

    # Technical Debt
    debt = analyses.get("debt", [])
    if debt:
        lines.append("\n### 🏗️ Critical Technical Debt:")
        high_debt = [d for d in debt if d.get("severity_score", 0) >= 4]
        for item in high_debt[:5]:
            lines.append(
                f"- **{item['module']}**: {item['total_issues']} issues (Score: {item['severity_score']})"
            )

    # Circular Dependencies
    deps = analyses.get("dependencies", {})
    circular = deps.get("circular_dependencies", [])
    if circular:
        lines.append("\n### 🔄 Circular Dependencies:")
        for cycle in circular[:3]:
            lines.append(
                f"- {' -> '.join(cycle) if isinstance(cycle, list) else str(cycle)}"
            )

    return "\n".join(lines)


def _build_qgis_compliance_section(analyses: Dict[str, Any]) -> str:
    """Builds the QGIS plugin standards compliance overview."""
    qgis = analyses.get("qgis_compliance", {})
    if not qgis:
        return ""

    lines = ["\n## 📦 QGIS PLUGIN STANDARDS"]
    lines.append(f"- **Compliance Score**: {qgis.get('compliance_score', 0):.1f}/100")

    mandatory = qgis.get("mandatory_files", {})
    missing = [f for f, exists in mandatory.get("files", {}).items() if not exists]
    if missing:
        lines.append(f"- ❌ **Missing Files**: {', '.join(missing)}")

    arch = qgis.get("architecture", {})
    violations = arch.get("violations", [])
    if violations:
        lines.append(f"- ⚠️ **Architecture**: {len(violations)} violations detected")
        for v in violations[:2]:
            lines.append(f"  - {v['file']}: {v['type']}")

    return "\n".join(lines)


def _build_recommendations_section(analyses: Dict[str, Any]) -> str:
    """Constructs the recommendations and optimizations section."""
    optimizations = analyses.get("optimizations", [])
    if not optimizations:
        return ""

    lines = ["\n## 💡 MAIN RECOMMENDATIONS"]
    for opt in optimizations[:3]:
        module_path = opt.get("module", "Unknown")
        lines.append(f"\n### {module_path}")
        for suggestion in opt.get("suggestions", [])[:2]:
            lines.append(f"- {suggestion.get('message', 'N/A')}")

    return "\n".join(lines)


def _build_patterns_summary_section(analyses: Dict[str, Any]) -> str:
    """Builds the Summary section for detected design patterns."""
    patterns = analyses.get("patterns", {})
    if not patterns:
        return ""

    sections = ["\n## 🏗️ DESIGN PATTERNS"]
    for name, occurrences in patterns.items():
        sections.append(f"\n### {name}")
        for occ in occurrences[:5]:
            sections.append(
                f"- **{occ['class']}** in `{occ['module']}` (Confidence: {occ['confidence']}%)"
            )

    return "\n".join(sections)


def _build_git_analysis_section(analyses: Dict[str, Any]) -> str:
    """Builds the Git analysis section (Hotspots and Churn)."""
    git = analyses.get("git", {})
    if not git:
        return ""

    sections = ["\n## 🔄 GIT ANALYSIS"]

    # Churn
    churn = git.get("churn", {})
    if churn.get("available"):
        sections.append(f"### Code Churn (last {churn.get('period_days')} days)")
        sections.append(f"- **Files Changed**: {churn.get('files_changed')}")
        sections.append(f"- **Additions**: +{churn.get('added')}")
        sections.append(f"- **Deletions**: -{churn.get('deleted')}")
        sections.append(f"- **Total Churn**: {churn.get('total_churn')}")

    # Hotspots
    hotspots = git.get("hotspots", [])
    if hotspots:
        sections.append("\n### 🔥 Hotspots (Frequently Changed Files)")
        for hs in hotspots:
            sections.append(f"- `{hs['path']}`: {hs['commits']} commits")

    return "\n".join(sections)


def _build_complexity_dist_section(analyses: Dict[str, Any]) -> str:
    """Creates the complexity distribution breakdown.

    Args:
        analyses: Results dictionary containing complexity distribution data.

    Returns:
        A Markdown-formatted string for the Complexity Distribution section.
    """
    complexity = analyses.get("complexity", {})
    dist = complexity.get("complexity_distribution", {})
    total = complexity.get("total_modules", 1) or 1

    sections = ["\n## 📈 COMPLEXITY DISTRIBUTION"]
    for key, value in dist.items():
        percentage = (value / total) * 100
        sections.append(f"- {key}: {value} modules ({percentage:.1f}%)")

    return "\n".join(sections)


def generate_ai_context(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
) -> None:
    """Generates an optimized project overview file for AI consumption.

    Focuses on structural elements, metrics, and patterns to help LLMs
    understand the codebase quickly.

    Args:
        analyses: Full analysis results dictionary.
        output_path: Path to save the AI context report.
        project_name: Human-readable project name.
    """
    structure = analyses.get("structure", {})
    entry_points = analyses.get("entry_points", [])
    complexity = analyses.get("complexity", {})
    dependencies = analyses.get("dependencies", {})

    context_lines = [
        f"# AI CONTEXT - {project_name}",
        "Automatically generated by Ai-Context-Core",
        "",
        "## 📁 PROJECT STRUCTURE",
        f"\n{structure.get('tree', 'N/A')[:1200]}\n",
        "",
        "## 🎯 ENTRY POINTS",
    ]

    for ep in entry_points[:10]:
        context_lines.append(f"- `{ep}`")
    if len(entry_points) > 10:
        context_lines.append(f"... and {len(entry_points) - 10} more")

    context_lines.append("\n## 🏗️ DETECTED PATTERNS")
    _add_patterns_section(analyses, context_lines)

    _add_antipatterns_section(analyses, context_lines)

    context_lines.append("\n## 📈 COMPLEXITY AND METRICS")
    context_lines.append(f"- **Total Modules**: {complexity.get('total_modules', 0)}")
    context_lines.append(f"- **Lines of Code**: {complexity.get('total_lines', 0):,}")
    context_lines.append(f"- **Functions**: {complexity.get('total_functions', 0)}")
    context_lines.append(f"- **Classes**: {complexity.get('total_classes', 0)}")
    context_lines.append(
        f"- **Average Complexity**: {complexity.get('average_complexity', 0):.1f}"
    )
    context_lines.append(
        f"- **Avg Maintenance Index**: {complexity.get('avg_maintenance_index', 0) or analyses.get('metrics', {}).get('avg_maintenance_index', 0):.1f}"
    )

    comp_mods = [m[0] for m in complexity.get("most_complex_modules", [])[:3]]
    context_lines.append(f"- **Most Complex Modules**: {', '.join(comp_mods)}")

    context_lines.append("\n## 🔗 PRIMARY DEPENDENCIES")
    _add_dependencies_section(dependencies, context_lines)

    _add_optimizations_section(analyses, context_lines)

    _add_dependency_insights_section(dependencies, context_lines)

    _add_dependency_graph_section(dependencies, context_lines)

    _add_git_context_section(analyses, context_lines)

    context_lines.append("\n## 🔑 PROJECT KEYWORDS")
    file_types = list(structure.get("file_types", {}).keys())
    context_lines.append(f"- **Technologies**: {', '.join(file_types[:8])}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(context_lines))


def _add_patterns_section(analyses: Dict[str, Any], lines: list):
    """Parses and adds detected design patterns to the context list.

    Args:
        analyses: Analysis results containing pattern detection data.
        lines: The list of context report lines to append to.
    """
    patterns = analyses.get("patterns", {})
    if not patterns:
        lines.append("No clear design patterns detected.")
        return

    for name, occurrences in patterns.items():
        lines.append(f"### {name}")
        for occ in occurrences[:3]:
            lines.append(
                f"- **{occ['class']}** in `{occ['module']}` (Confidence: {occ['confidence']}%)"
            )
            for ev in occ.get("evidence", []):
                lines.append(f"  - _Evidence: {ev}_")


def _add_dependencies_section(dependencies: Dict[str, Any], lines: list):
    """Categorizes and summarizes external dependencies for the context report.

    Args:
        dependencies: Dependency analysis results.
        lines: The list of context report lines to append to.
    """
    third_party = dependencies.get("third_party", [])
    if third_party:
        base_packages = {}
        for dep in third_party:
            base = dep.split(".")[0]
            base_packages[base] = base_packages.get(base, 0) + 1

        lines.append("\n### Third Party (most frequent):")
        sorted_pkgs = sorted(base_packages.items(), key=lambda x: x[1], reverse=True)[
            :15
        ]
        for package, count in sorted_pkgs:
            lines.append(f"- `{package}` ({count} imports)")


def _add_optimizations_section(analyses: Dict[str, Any], lines: list):
    """Extracts top optimization opportunities for the context report.

    Args:
        analyses: Full analysis results.
        lines: The list of context report lines to append to.
    """
    optimizations = analyses.get("optimizations", [])
    if optimizations:
        lines.append("\n## 💡 OPTIMIZATION RECOMMENDATIONS")
        for opt in optimizations[:5]:
            module = opt.get("module", "Unknown")
            lines.append(f"\n### {module}")
            for suggestion in opt.get("suggestions", [])[:2]:
                lines.append(
                    f"- **{suggestion.get('type', 'Opt')}**: {suggestion.get('message', 'N/A')}"
                )


def _add_dependency_insights_section(dependencies: Dict[str, Any], lines: list):
    """Adds advanced dependency insights like unused imports and coupling."""
    unused = dependencies.get("unused_imports", {})
    if unused:
        lines.append("\n## ⚠️ UNUSED IMPORTS")
        # Show top 5 modules with unused imports
        for mod, items in list(unused.items())[:5]:
            lines.append(f"- **{mod}**: {', '.join(items[:5])}")

    coupling = dependencies.get("coupling_metrics", {})
    if coupling:
        high_coupling = sorted(
            coupling.items(), key=lambda x: x[1].get("cbo", 0), reverse=True
        )[:5]
        # Only show if CBO is significant
        high_coupling = [item for item in high_coupling if item[1].get("cbo", 0) > 5]

        if high_coupling:
            lines.append("\n## 🔗 HIGH COUPLING MODULES (CBO)")
            for mod, m in high_coupling:
                lines.append(
                    f"- **{mod}**: CBO {m['cbo']} (In: {m['fan_in']}, Out: {m['fan_out']})"
                )


def _add_dependency_graph_section(dependencies: Dict[str, Any], lines: list):
    """Appends dependency graph statistics and the Mermaid diagram.

    Args:
        dependencies: Dependency analysis data.
        lines: The list of context report lines to append to.
    """
    metrics = dependencies.get("graph_metrics", {})
    if metrics:
        lines.append("\n## 🕸️  DEPENDENCY STRUCTURE")
        lines.append(f"- **Nodes**: {metrics.get('nodes', 0)}")
        lines.append(f"- **Edges**: {metrics.get('edges', 0)}")
        lines.append(f"- **Density**: {metrics.get('density', 0):.3f}")
        lines.append(f"- **Acyclic Graph**: {'Yes' if metrics.get('is_dag') else 'No'}")
        lines.append(
            f"- **Connected Components**: {metrics.get('weakly_connected_components', 0)}"
        )

        lines.append("\n## 🕸️ DEPENDENCY DIAGRAM (Conceptual)")
        lines.append("```mermaid")
        lines.append(generate_mermaid_graph(dependencies))
        lines.append("```")


def _add_antipatterns_section(analyses: Dict[str, Any], lines: list):
    """Adds detected anti-patterns to the context report.

    Args:
        analyses: Analysis results containing antipatterns data.
        lines: The list of context report lines to append to.
    """
    antipatterns = analyses.get("antipatterns", [])
    if antipatterns:
        lines.append("\n## ⚠️ DETECTED ANTI-PATTERNS")
        for item in antipatterns[:5]:
            module = item.get("module", "Unknown")
            lines.append(f"- **{module}**")
            for issue in item.get("issues", [])[:2]:
                lines.append(f"  - {issue.get('message', 'N/A')}")


def _add_git_context_section(analyses: Dict[str, Any], lines: list):
    """Adds git context like hotspots and churn to the AI context."""
    git = analyses.get("git", {})
    if not git:
        return

    lines.append("\n## 🔄 GIT AND EVOLUTION")

    # Hotspots are very useful for AI context
    hotspots = git.get("hotspots", [])
    if hotspots:
        lines.append("### Top Hotspots (High change frequency):")
        for hs in hotspots:
            lines.append(f"- `{hs['path']}` ({hs['commits']} commits)")

    churn = git.get("churn", {})
    if churn.get("available"):
        lines.append(f"### Recent Churn ({churn.get('period_days')} days):")
        lines.append(f"- Total lines changed: {churn.get('total_churn')}")
