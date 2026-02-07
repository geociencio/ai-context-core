"""File system utilities and cache management.

Provides optimized file reading, exclusion pattern handling, and
project structure generation (tree view) with LRU caching.
"""

import pathlib
import logging
from typing import Dict, Any
from .fs_scanner import scan_project
from .fs_helpers import load_exclusion_patterns, calculate_file_hash
from .fs_cache import load_cache, save_cache
from .gis_utils import parse_qgis_metadata
from .fs_tree import generate_tree_optimized

logger = logging.getLogger(__name__)

# Helper for backward compatibility
def count_file_types(project_path: pathlib.Path) -> Dict[str, int]:
    return scan_project(project_path, []).file_types

def calculate_size_stats(project_path: pathlib.Path) -> Dict[str, Any]:
    return scan_project(project_path, []).size_stats
