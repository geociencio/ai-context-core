"""Metrics summarizer for project analysis."""

from typing import Dict, Any


class MetricsSummarizer:
    """Summarizes project metrics for reporting."""

    def __init__(self, analyses: Dict[str, Any]):
        """Initialize with analysis results."""
        self.analyses = analyses

    def build_metrics(self) -> str:
        """Build metrics section."""
        metrics = self.analyses.get("metrics", {})

        lines = []
        lines.append(f"- **Quality Score**: {metrics.get('quality_score', 0):.1f}/100")
        lines.append(
            f"- **Source Lines (SLOC)**: {metrics.get('total_lines_code', 0):,}"
        )
        lines.append(
            f"- **Total Physical Lines**: {metrics.get('total_physical_lines', 0):,}"
        )
        lines.append(
            f"- **Maintainability**: {metrics.get('avg_maintainability', 0):.1f}"
        )
        lines.append(
            f"- **Test Coverage**: {metrics.get('test_files_count', 0)} test files"
        )

        return "\n".join(lines)

    def build_structure(self) -> str:
        """Build project structure section."""
        struct = self.analyses.get("structure", {})
        tree = struct.get("tree", "")
        if not tree:
            return "No tree structure available."

        lines = []
        lines.append(f"**Total Modules**: {struct.get('modules_count', 0)}")
        lines.append("\n```tree")
        lines.append(tree)
        lines.append("```")

        return "\n".join(lines)

    def build_complexity(self) -> str:
        """Build complexity analysis section."""
        comp = self.analyses.get("complexity", {})
        metrics = self.analyses.get("metrics", {})

        lines = []
        lines.append(
            f"- **Average Complexity**: {metrics.get('avg_complexity', 0):.2f}"
        )
        lines.append(f"- **Max Complexity**: {metrics.get('max_complexity', 0)}")

        high = comp.get("high_complexity", [])
        if high:
            lines.append("\n**Top Complex Modules**:")
            for m in high[:5]:
                lines.append(f"- `{m['name']}`: {m['complexity']}")

        return "\n".join(lines)
