"""File system utilities and cache management.

Provides optimized file reading, exclusion pattern handling, and
project structure generation (tree view) with LRU caching.
"""

import pathlib
import logging
from typing import Dict, Any
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
    "count_file_types",
    "calculate_size_stats",
    "get_file_stats",
]

logger = logging.getLogger(__name__)


# Helper for backward compatibility
def count_file_types(project_path: pathlib.Path) -> Dict[str, int]:
    """Count file extensions in the project.

    Args:
        project_path: Path to the project root.

    Returns:
        Dictionary mapping file extensions to their counts.

    """
    return scan_project(project_path, []).file_types


def calculate_size_stats(project_path: pathlib.Path) -> Dict[str, Any]:
    """Calculate size statistics for the project.

    Args:
        project_path: Path to the project root.

    Returns:
        Dictionary containing total size and file count statistics.

    """
    return scan_project(project_path, []).size_stats
