"""Summary generation utilities for ai-context-core reporting.

Context-only (v5.0.0): the summary is markdown-only and no longer embeds QGIS,
design-pattern or HTML-dashboard sections.
"""

import pathlib
from typing import Any, Dict


class ProjectSummaryGenerator:
    """Orchestrates the generation of the project summary.

    Uses specialized summarizers to compose the report sections.
    """

    def __init__(self, analyses: Dict[str, Any], project_name: str):
        """Initialize the generator.

        Args:
            analyses: Dictionary of project analysis results.
            project_name: The name of the project.
        """
        self.analyses = analyses
        self.project_name = project_name
        from . import GitSummarizer, IssuesSummarizer, MetricsSummarizer

        self.metrics_s = MetricsSummarizer(analyses)
        self.issues_s = IssuesSummarizer(analyses)
        self.git_s = GitSummarizer(analyses)

    def generate_markdown(self, output_path: pathlib.Path):
        """Generate the Markdown project summary.

        Args:
            output_path: Path where the Markdown report will be saved.
        """
        from .reporting import MarkdownBuilder

        builder = MarkdownBuilder(f"PROJECT SUMMARY - {self.project_name}")

        sections = [
            ("📊 KEY METRICS", self.metrics_s.build_metrics()),
            ("📁 STRUCTURE", self.metrics_s.build_structure()),
            ("🚨 CRITICAL ISSUES", self.issues_s.build_issues()),
            ("💡 MAIN RECOMMENDATIONS", self.issues_s.build_recommendations()),
            ("📝 ARCHITECTURE NOTES", self._build_manual_notes()),
            ("🔄 GIT ANALYSIS", self.git_s.build_git()),
            ("📈 COMPLEXITY DISTRIBUTION", self.metrics_s.build_complexity()),
        ]

        for title, content in sections:
            if content:
                builder.add_section(title, content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(builder.build())

    def _build_manual_notes(self) -> str:
        """Return the manual architecture notes embedded in the analysis."""
        return self.analyses.get("manual_notes", "")


# Alias for backward compatibility
SummaryGenerator = ProjectSummaryGenerator
