"""Summary generation utilities for ai-context-core reporting."""

import pathlib
from typing import Dict, Any
from .html_builder import HTMLReportBuilder


class ProjectSummaryGenerator:
    """Orchestrates the generation of project summaries in different formats.

    Uses specialized summarizers to build sections of the reports, following
    the strategy pattern for report composition.
    """

    def __init__(self, analyses: Dict[str, Any], project_name: str):
        """Initialize the generator.

        Args:
            analyses: Dictionary of project analysis results.
            project_name: The name of the project.
        """
        self.analyses = analyses
        self.project_name = project_name
        from . import (
            MetricsSummarizer,
            IssuesSummarizer,
            QGISSummarizer,
            GitPatternsSummarizer,
        )

        self.metrics_s = MetricsSummarizer(analyses)
        self.issues_s = IssuesSummarizer(analyses)
        self.qgis_s = QGISSummarizer(analyses)
        self.git_p_s = GitPatternsSummarizer(analyses)

    def generate_html(self, output_path: pathlib.Path):
        """Generates the HTML report.

        Args:
            output_path: Path where the HTML report will be saved.
        """
        builder = HTMLReportBuilder(f"PROJECT SUMMARY - {self.project_name}")

        # Metrics
        m = self.analyses.get("metrics", {})
        c = self.analyses.get("complexity", {})
        m_html = f"""
        <div class="metric">Quality Score: <span class="metric-value">{m.get("quality_score", 0)}/100</span></div>
        <div class="metric">Source Lines (SLOC): <span class="metric-value">{m.get("total_lines_code", 0):,}</span></div>
        <div class="metric">Physical Lines: <span class="metric-value">{m.get("total_physical_lines", 0):,}</span></div>
        <div class="metric">Modules: <span class="metric-value">{c.get("total_modules", 0)}</span></div>
        """
        builder.add_section("📊 KEY METRICS", m_html)

        # Issues
        sec = self.analyses.get("security", [])
        if sec:
            s_list = [
                f"<strong>{i['module']}</strong>: {i['total_issues']} issues (Max: {i['max_severity']})"
                for i in sec[:5]
            ]
            builder.add_section("🚨 SECURITY ISSUES", builder.build_list(s_list))

        # Recommendations
        opt = self.analyses.get("optimizations", [])
        if opt:
            o_list = [
                f"<strong>{o['module']}</strong>: {'; '.join(s.get('message', '') for s in o.get('suggestions', []))}"
                for o in opt[:5]
            ]
            builder.add_section("💡 RECOMMENDATIONS", builder.build_list(o_list))

        # Graph
        from .reporting import generate_dependency_diagram

        graph = generate_dependency_diagram(self.analyses.get("dependencies", {}))
        if graph:
            builder.add_section(
                "🕸️ DEPENDENCY GRAPH", f'<div class="mermaid">{graph}</div>'
            )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(builder.render())

    def generate_markdown(self, output_path: pathlib.Path):
        """Generates the Markdown report.

        Args:
            output_path: Path where the Markdown report will be saved.
        """
        from .reporting import MarkdownBuilder

        builder = MarkdownBuilder(f"PROJECT SUMMARY - {self.project_name}")

        sections = [
            ("📊 KEY METRICS", self.metrics_s.build_metrics()),
            ("📁 STRUCTURE", self.metrics_s.build_structure()),
            ("🚨 CRITICAL ISSUES", self.issues_s.build_issues()),
            ("📦 QGIS STANDARDS", self.qgis_s.build()),
            ("💡 MAIN RECOMMENDATIONS", self.issues_s.build_recommendations()),
            ("🏗️ DESIGN PATTERNS", self.git_p_s.build_patterns()),
            ("📝 ARCHITECTURE NOTES", self._build_manual_notes()),
            ("🔄 GIT ANALYSIS", self.git_p_s.build_git()),
            ("📈 COMPLEXITY DISTRIBUTION", self.metrics_s.build_complexity()),
        ]

        for title, content in sections:
            if content:
                builder.add_section(title, content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(builder.build())

    def _build_manual_notes(self) -> str:
        """Reads manual architecture notes from the project configuration."""
        return self.analyses.get("manual_notes", "")


# Alias for backward compatibility
SummaryGenerator = ProjectSummaryGenerator
