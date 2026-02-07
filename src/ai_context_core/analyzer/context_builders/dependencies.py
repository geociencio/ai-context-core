"""Builders for dependencies and optimizations."""

from .base import BaseContextBuilder
from typing import List


class DependencyBuilder(BaseContextBuilder):
    """Adds dependency analysis and optimizations."""

    def build(self, lines: List[str]) -> None:
        from ..reporting import generate_dependency_diagram

        deps = self.analyses.get("dependencies", {})
        lines.append("\n## 🔗 PRIMARY DEPENDENCIES")
        tp = deps.get("third_party", [])
        if tp:
            counts = {}
            for d in tp:
                base = d.split(".")[0]
                counts[base] = counts.get(base, 0) + 1
            lines.append("### Third Party (most frequent):")
            for p, c in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:15]:
                lines.append(f"- `{p}` ({c} imports)")

        unused = deps.get("unused_imports", {})
        if unused:
            lines.append("\n## ⚠️ UNUSED IMPORTS")
            for mod, items in list(unused.items())[:5]:
                lines.append(f"- **{mod}**: {', '.join(items[:5])}")

        high_c = sorted(
            deps.get("coupling_metrics", {}).items(),
            key=lambda x: x[1].get("cbo", 0),
            reverse=True,
        )[:5]
        high_c = [i for i in high_c if i[1].get("cbo", 0) > 5]
        if high_c:
            lines.append("\n## 🔗 HIGH COUPLING MODULES (CBO)")
            for mod, m_val in high_c:
                lines.append(
                    f"- **{mod}**: CBO {m_val['cbo']} (In: {m_val['fan_in']}, Out: {m_val['fan_out']})"
                )

        g_m = deps.get("graph_metrics", {})
        if g_m:
            lines.append("\n## 🕸️  DEPENDENCY STRUCTURE")
            lines.append(
                f"- **Nodes**: {g_m.get('nodes', 0)}\n- **Edges**: {g_m.get('edges', 0)}\n- **Density**: {g_m.get('density', 0):.3f}"
            )
            lines.append("\n## 🕸️ DEPENDENCY DIAGRAM (Conceptual)\n```mermaid")
            lines.append(generate_dependency_diagram(deps))
            lines.append("```")

        # Optimizations (also related to technical debt/dependencies)
        opts = self.analyses.get("optimizations", [])
        if opts:
            lines.append("\n## 💡 OPTIMIZATION RECOMMENDATIONS")
            for o in opts[:5]:
                lines.append(f"### {o.get('module')}")
                for sug in o.get("suggestions", [])[:2]:
                    lines.append(
                        f"- **{sug.get('type', 'Opt')}**: {sug.get('message', 'N/A')}"
                    )
