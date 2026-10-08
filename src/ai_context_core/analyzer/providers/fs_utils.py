"""File system utilities and cache management.

Provides optimized file reading, exclusion pattern handling, and
project structure generation (tree view) with LRU caching.
"""

import logging
from .fs_scanner import scan_project
from .fs_cache import load_cache, save_cache  # noqa: F401
from .gis_utils import parse_qgis_metadata  # noqa: F401
from .fs_tree import generate_tree_optimized  # noqa: F401
from .fs_helpers import (
    load_exclusion_patterns,
    calculate_file_hash,
    read_file_fast,
    get_file_stats,
)

__all__ = [
    "scan_project",
    "load_cache",
    "save_cache",
    "parse_qgis_metadata",
    "generate_tree_optimized",
    "load_exclusion_patterns",
    "calculate_file_hash",
    "read_file_fast",
    "get_file_stats",
]

logger = logging.getLogger(__name__)
