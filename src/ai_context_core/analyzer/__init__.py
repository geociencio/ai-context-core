from .. import __version__
from .engine import ProjectAnalyzer
from .providers import (
    fs_utils,
    git_analysis,
    gis_utils,
    worker,
)
from .builders import (
    aggregator,
    reporting,
    ai_recommendations,
    dependencies,
    issues as builder_issues,  # noqa: F401
)
from .visitors import (
    ast_utils,
    antipatterns,
    issues as visitor_issues,
)

# For backward compatibility with existing tests and CLI imports
AnalysisWorker = worker.AnalysisWorker
graph_engine = dependencies
issues = visitor_issues  # Typically tests expect the detectors here

__all__ = [
    "ProjectAnalyzer",
    "AnalysisWorker",
    "fs_utils",
    "git_analysis",
    "gis_utils",
    "aggregator",
    "dependencies",
    "reporting",
    "ai_recommendations",
    "ast_utils",
    "antipatterns",
    "issues",
    "__version__",
]
