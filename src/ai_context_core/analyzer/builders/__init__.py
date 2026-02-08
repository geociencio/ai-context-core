"""Results aggregation, report generation, and context building."""

from .reporting import (
    generate_project_summary,
    generate_ai_context,
)
from .aggregator import ResultsAggregator
from .dependencies import DependencyAnalyzer, DependencyBuilder
from .html_builder import HTMLReportBuilder
from .summary_generator import ProjectSummaryGenerator
from .ai_context_generator import AIContextGenerator
from .ai_recommendations import generate_recommendations
from .metrics_summarizer import MetricsSummarizer
from .issues import IssuesSummarizer
from .aggregator_qgis import QGISSummarizer
from .git_patterns import GitPatternsSummarizer
from .structure import StructureBuilder
from .context_metrics import MetricsBuilder
from .patterns import PatternsBuilder
from .git_tech import GitTechBuilder

__all__ = [
    "generate_project_summary",
    "generate_ai_context",
    "ResultsAggregator",
    "DependencyAnalyzer",
    "DependencyBuilder",
    "HTMLReportBuilder",
    "ProjectSummaryGenerator",
    "AIContextGenerator",
    "generate_recommendations",
    "MetricsSummarizer",
    "IssuesSummarizer",
    "QGISSummarizer",
    "GitPatternsSummarizer",
    "StructureBuilder",
    "MetricsBuilder",
    "PatternsBuilder",
    "GitTechBuilder",
]
