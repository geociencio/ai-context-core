"""Results aggregation, report generation, and context building."""

from .reporting import (
    generate_project_summary,
    generate_ai_context,
)
from .aggregator import ResultsAggregator
from .dependencies import DependencyAnalyzer, DependencyBuilder
from .summary_generator import ProjectSummaryGenerator
from .ai_context_generator import AIContextGenerator
from .metrics_summarizer import MetricsSummarizer
from .issues import IssuesSummarizer
from .structure import StructureBuilder
from .context_metrics import MetricsBuilder
from .git_tech import GitTechBuilder

__all__ = [
    "generate_project_summary",
    "generate_ai_context",
    "ResultsAggregator",
    "DependencyAnalyzer",
    "DependencyBuilder",
    "ProjectSummaryGenerator",
    "AIContextGenerator",
    "MetricsSummarizer",
    "IssuesSummarizer",
    "StructureBuilder",
    "MetricsBuilder",
    "GitTechBuilder",
]
