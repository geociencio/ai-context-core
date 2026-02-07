"""File system utilities and cache management.

Provides optimized file reading, exclusion pattern handling, and
project structure generation (tree view) with LRU caching.
"""

import os
import pathlib
import mmap
import subprocess
import logging
import hashlib
import json
from typing import List, Dict, Any, NamedTuple
from collections import OrderedDict
from .ignore_filter import IgnoreFilter

logger = logging.getLogger(__name__)


from .fs_scanner import ProjectScanResult, ProjectScanner, scan_project
from .fs_cache import LRUCache, file_cache, load_cache, save_cache
from .fs_tree import generate_tree_optimized, analyze_structure
from .fs_helpers import read_file_fast, is_test_file, calculate_file_hash, load_exclusion_patterns
from .gis_utils import parse_qgis_metadata

# Helper for backward compatibility
def count_file_types(project_path: pathlib.Path) -> Dict[str, int]:
    return scan_project(project_path, []).file_types

def calculate_size_stats(project_path: pathlib.Path) -> Dict[str, Any]:
    return scan_project(project_path, []).size_stats
