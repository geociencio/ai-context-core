"""Analyzer engine package (context-only, v5.0.0)."""

from .. import __version__
from .builders import (
    aggregator,
    dependencies,
    reporting,
)
from .engine import ProjectAnalyzer
from .providers import (
    fs_utils,
    git_analysis,
    gis_utils,
    worker,
)
from .visitors import ast_utils

# For backward compatibility with existing tests and CLI imports
AnalysisWorker = worker.AnalysisWorker
graph_engine = dependencies

__all__ = [
    "ProjectAnalyzer",
    "AnalysisWorker",
    "fs_utils",
    "git_analysis",
    "gis_utils",
    "aggregator",
    "dependencies",
    "reporting",
    "ast_utils",
    "__version__",
]
