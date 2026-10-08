"""Metrics summarizer for project analysis."""

from typing import Dict, Any

from . import metric_keys


class MetricsSummarizer:
    """Summarizes project metrics for reporting."""

    def __init__(self, analyses: Dict[str, Any]):
        """Initialize with analysis results."""
        self.analyses = analyses

    def build_metrics(self) -> str:
        """Build metrics section."""
        metrics = self.analyses.get("metrics", {})

        lines = []
        lines.append(
            f"- **ai-ctx Quality Score**: {metrics.get(metric_keys.QUALITY_SCORE, 0):.1f}/100"
        )
        lines.append(
            f"- **Source Lines (SLOC)**: {metrics.get(metric_keys.TOTAL_LINES_CODE, 0):,}"
        )
        lines.append(
            f"- **Total Physical Lines**: "
            f"{metrics.get(metric_keys.TOTAL_PHYSICAL_LINES, 0):,}"
        )
        lines.append(
            f"- **Maintainability**: "
            f"{metrics.get(metric_keys.AVG_MAINTENANCE_INDEX, 0):.1f}"
        )
        test_count = metrics.get(metric_keys.TEST_FILES_COUNT)
        test_display = "n/a" if test_count is None else f"{test_count} test files"
        lines.append(f"- **Test Files**: {test_display}")
        lines.append(
            "- _Note: the ai-ctx Quality Score is a heuristic, non-canonical metric._"
        )

        breakdown = metrics.get(metric_keys.SCORE_BREAKDOWN) or {}
        if breakdown:
            lines.append("\n**Score Breakdown**:")
            lines.append(f"- Base: {breakdown.get('base', 0):.0f}")
            for label, key in (
                ("Complexity (avg)", "complexity"),
                ("Complexity (max)", "max_complexity"),
                ("Maintainability", "maintainability"),
                ("Tests", "tests"),
            ):
                value = breakdown.get(key, 0)
                if value:
                    lines.append(f"- {label}: {value:+.1f}")

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
            f"- **Avg Cyclomatic Complexity**: "
            f"{metrics.get(metric_keys.AVERAGE_COMPLEXITY, 0):.2f}"
        )
        lines.append(
            f"- **Max Complexity**: {metrics.get(metric_keys.MAX_COMPLEXITY, 0)}"
        )

        high = comp.get("high_complexity", [])
        if high:
            lines.append("\n**Top Complex Modules**:")
            for m in high[:5]:
                lines.append(f"- `{m['name']}`: {m['complexity']}")

        return "\n".join(lines)
