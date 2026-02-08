"""Infrastructure and data providers (Filesystem, Git, Config, Engine)."""

from .fs_utils import (
    scan_project,
    get_file_stats,
    calculate_file_hash,
    save_cache,
    load_cache,
    read_file_fast,
    parse_qgis_metadata,
)
from .fs_scanner import scan_project as scan_project_alt  # noqa: F401
from .fs_tree import generate_tree_optimized
from .fs_cache import LRUCache
from .ignore_filter import IgnoreFilter
from .loader import load_ignore_patterns
from .compiler import compile_ignore_patterns
from .git_analysis import analyze_git_evolution
from .worker import AnalysisWorker
from .config_loader import load_config

__all__ = [
    "scan_project",
    "get_file_stats",
    "calculate_file_hash",
    "save_cache",
    "load_cache",
    "read_file_fast",
    "parse_qgis_metadata",
    "generate_tree_optimized",
    "LRUCache",
    "IgnoreFilter",
    "load_ignore_patterns",
    "compile_ignore_patterns",
    "analyze_git_evolution",
    "AnalysisWorker",
    "load_config",
]
