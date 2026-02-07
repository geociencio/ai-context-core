"""Summarizers for metrics, structure, and complexity."""

from .base import BaseSummarizer

class MetricsSummarizer(BaseSummarizer):
    """Builds metrics and structure sections."""

    def build_metrics(self) -> str:
        c = self.analyses.get("complexity", {})
        m = self.analyses.get("metrics", {})
        s = self.analyses.get("structure", {}).get("size_stats", {})
        return (
            f"- **Total Modules**: {c.get('total_modules', 0):,}\n"
            f"- **Source Lines (SLOC)**: {c.get('total_lines', 0):,}\n"
            f"- **Total Physical Lines**: {m.get('total_physical_lines', 0):,}\n"
            f"- **Total Size**: {s.get('total_size_mb', 0):.1f} MB\n"
            f"- **Average Complexity**: {c.get('average_complexity', 0):.1f}\n"
            f"- **Avg Maintenance Index**: {m.get('avg_maintenance_index', 0):.1f}\n"
            f"- **Docstring Coverage**: {m.get('docstring_coverage', 0):.1f}%\n"
            f"- **Quality Score**: {m.get('quality_score', 0):.1f}/100\n"
            f"- **Test Files**: {m.get('test_files_count', 0)}"
        )

    def build_structure(self) -> str:
        s = self.analyses.get("structure", {})
        sz = s.get("size_stats", {})
        ft = list(s.get("file_types", {}).keys())
        return (
            f"- **Python Files**: {sz.get('python_files', 0)}\n"
            f"- **Total Files**: {sz.get('total_files', 0)}\n"
            f"- **Primary File Types**: {', '.join(ft[:5])}"
        )

    def build_complexity(self) -> str:
        c = self.analyses.get("complexity", {})
        dist = c.get("complexity_distribution", {})
        total = c.get("total_modules", 1) or 1
        return "\n".join(
            f"- {k}: {v} modules ({v / total * 100:.1f}%)" for k, v in dist.items()
        )
