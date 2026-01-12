import pathlib
import time
from typing import Dict, Any


def generate_mermaid_graph(dependencies: Dict[str, Any]) -> str:
    """Genera diagrama Mermaid de dependencias principales."""
    graph = ["graph TD"]
    import_graph = dependencies.get("import_graph", {})
    node_scores = {u: len(v) for u, v in import_graph.items()}
    top_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)[:15]
    top_node_names = {name for name, _ in top_nodes}

    for u, neighbors in import_graph.items():
        if u in top_node_names:
            u_short = u.split("/")[-1].replace(".py", "")
            for v in neighbors:
                v_short = v.split(".")[-1]
                if any(top_name in v for top_name in top_node_names):
                    graph.append(f"    {u_short} --> {v_short}")

    return "\n".join(graph[:30])


def generate_project_summary(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
) -> None:
    """Generates an executive summary of the project."""
    structure = analyses.get("structure", {})
    complexity = analyses.get("complexity", {})
    metrics = analyses.get("metrics", {})
    dependencies = analyses.get("dependencies", {})

    summary_content = f"""# PROJECT SUMMARY - {project_name}
Analysis Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: {complexity.get("total_modules", 0):,}
- **Lines of Code**: {complexity.get("total_lines", 0):,}
- **Total Size**: {structure.get("size_stats", {}).get("total_size_mb", 0):.1f} MB
- **Average Complexity**: {complexity.get("average_complexity", 0):.1f}
- **Docstring Coverage**: {metrics.get("docstring_coverage", 0):.1f}%
- **Quality Score**: {metrics.get("quality_score", 0):.1f}/100
- **Test Files**: {metrics.get("test_files_count", 0)}

## 📁 STRUCTURE
- **Python Files**: {structure.get("size_stats", {}).get("python_files", 0)}
- **Total Files**: {structure.get("size_stats", {}).get("total_files", 0)}
- **Primary File Types**: {", ".join(list(structure.get("file_types", {}).keys())[:5])}

## 🚨 CRITICAL ISSUES
"""

    # Add security issues
    security = analyses.get("security", [])
    if security:
        summary_content += "\n### 🔒 Security Issues:\n"
        high_security = [s for s in security if s.get("max_severity") == "alta"]
        for item in high_security[:3]:
            summary_content += (
                f"- **{item['module']}**: {item['total_issues']} critical issues\n"
            )

    # Add technical debt
    debt = analyses.get("debt", [])
    if debt:
        summary_content += "\n### 🏗️ Critical Technical Debt:\n"
        high_debt = [d for d in debt if d.get("severity_score", 0) >= 5]
        for item in high_debt[:5]:
            summary_content += f"- **{item['module']}**: {item['total_issues']} issues (score: {item['severity_score']})\n"

    # Add circular dependencies
    circular = dependencies.get("circular_dependencies", [])
    if circular:
        summary_content += "\n### 🔄 Circular Dependencies:\n"
        for cycle in circular[:3]:
            summary_content += f"- {cycle}\n"

    # Add QGIS compliance
    qgis = analyses.get("qgis_compliance", {})
    if qgis:
        summary_content += "\n## 📦 QGIS PLUGIN STANDARDS\n"
        summary_content += (
            f"- **Compliance Score**: {qgis.get('compliance_score', 0):.1f}/100\n"
        )

        # Missing files
        mandatory = qgis.get("mandatory_files", {})
        missing = [f for f, exists in mandatory.get("files", {}).items() if not exists]
        if missing:
            summary_content += f"- ❌ **Missing Files**: {', '.join(missing)}\n"

        # Architecture violations
        arch = qgis.get("architecture", {})
        if arch.get("violations"):
            violations = arch["violations"]
            summary_content += (
                f"- ⚠️ **Architecture**: {len(violations)} violations detected (UI/Core mix)\n"
            )
            for v in violations[:2]:
                summary_content += f"  - {v['file']}: {v['type']}\n"

        # Widget recommendations
        widgets = qgis.get("widgets", {})
        if widgets.get("recommendations"):
            summary_content += f"- 💡 **UI Enhancement**: {len(widgets['recommendations'])} generic components could be QGIS widgets\n"

        # Performance
        perf = qgis.get("performance", {})
        if perf.get("issues"):
            summary_content += f"- ⚡ **Optimization**: {len(perf['issues'])} PyQGIS performance patterns detected\n"

    # Add recommendations
    optimizations = analyses.get("optimizations", [])
    if optimizations:
        summary_content += "\n## 💡 MAIN RECOMMENDATIONS\n"
        high_priority = [o for o in optimizations if o.get("priority") == "alta"]
        for opt in high_priority[:3]:
            summary_content += f"\n### {opt['module']}\n"
            for suggestion in opt["suggestions"][:2]:
                summary_content += f"- {suggestion['message']}\n"

    summary_content += "\n## 📈 COMPLEXITY DISTRIBUTION\n"
    dist = complexity.get("complexity_distribution", {})
    for key, value in dist.items():
        percentage = (value / complexity.get("total_modules", 1)) * 100
        summary_content += f"- {key}: {value} modules ({percentage:.1f}%)\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary_content)


def generate_ai_context(
    analyses: Dict[str, Any], output_path: pathlib.Path, project_name: str
) -> None:
    """Generates optimized context for AI."""
    structure = analyses.get("structure", {})
    entry_points = analyses.get("entry_points", [])
    patterns = analyses.get("patterns", {})
    complexity = analyses.get("complexity", {})
    dependencies = analyses.get("dependencies", {})

    extra_eps = f"\n... and {len(entry_points) - 10} more" if len(entry_points) > 10 else ""
    context_content = f"""# AI CONTEXT - {project_name}
Automatically generated by Ai-Context-Core
## 📁 PROJECT STRUCTURE

{structure.get("tree", "Not available")[:1200]}


## 🎯 ENTRY POINTS
{chr(10).join(f"- `{ep}`" for ep in entry_points[:10])}
{extra_eps}

## 🏗️ DETECTED PATTERNS
"""

    # List patterns found
    detected_patterns = []
    for pattern_name, pattern_data in patterns.items():
        if isinstance(pattern_data, dict) and pattern_data.get("detected"):
            confidence = pattern_data.get("confidence", 0)
            detected_patterns.append(
                f"- **{pattern_name.upper()}**: Detected (confidence: {confidence:.0%})"
            )

    if detected_patterns:
        context_content += "\n".join(detected_patterns)
    else:
        context_content += "\nNo clear design patterns detected."

    context_content += f"""
## 📈 COMPLEXITY AND METRICS
- **Total Modules**: {complexity.get("total_modules", 0)}
- **Lines of Code**: {complexity.get("total_lines", 0):,}
- **Functions**: {complexity.get("total_functions", 0)}
- **Classes**: {complexity.get("total_classes", 0)}
- **Average Complexity**: {complexity.get("average_complexity", 0):.1f}
- **Most Complex Modules**: {", ".join([m[0] for m in complexity.get("most_complex_modules", [])[:3]])}

## 🔗 PRIMARY DEPENDENCIES
"""

    # Add primary dependencies
    third_party = dependencies.get("third_party", [])
    if third_party:
        # Group by base package
        base_packages = {}
        for dep in third_party:
            base = dep.split(".")[0]
            base_packages[base] = base_packages.get(base, 0) + 1

        context_content += "\n### Third Party (most frequent):\n"
        for package, count in sorted(base_packages.items(), key=lambda x: x[1], reverse=True)[:15]:
            context_content += f"- `{package}` ({count} imports)\n"

    # Add main recommendations
    optimizations = analyses.get("optimizations", [])
    if optimizations:
        context_content += "\n## 💡 OPTIMIZATION RECOMMENDATIONS\n"
        for opt in optimizations[:5]:
            context_content += f"\n### {opt['module']} (Priority: {opt['priority'].upper()})\n"
            for suggestion in opt["suggestions"][:2]:
                context_content += f"- **{suggestion['type']}**: {suggestion['message']}\n"

    # Add dependency structure
    graph_metrics = dependencies.get("graph_metrics", {})
    if graph_metrics:
        context_content += f"""
## 🕸️  DEPENDENCY STRUCTURE
- **Nodes**: {graph_metrics.get("nodes", 0)}
- **Edges**: {graph_metrics.get("edges", 0)}
- **Density**: {graph_metrics.get("density", 0):.3f}
- **Acyclic Graph**: {"Yes" if graph_metrics.get("is_dag", False) else "No"}
- **Connected Components**: {graph_metrics.get("weakly_connected_components", 0)}

## 🕸️ DEPENDENCY DIAGRAM (Conceptual)
```mermaid
{generate_mermaid_graph(dependencies)}
```

## 🔑 PROJECT KEYWORDS
"""
    # Summary of file types and detected patterns
    context_content += (
        "- **Technologies**: " + ", ".join(list(structure.get("file_types", {}).keys())[:8]) + "\n"
    )
    context_content += (
        "- **Patterns**: "
        + ", ".join([p for p, d in patterns.items() if isinstance(d, dict) and d.get("detected")])
        + "\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(context_content)

