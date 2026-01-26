"""File system utilities and cache management.

Provides optimized file reading, exclusion pattern handling, and
project structure generation (tree view) with LRU caching.
"""

import os
import pathlib
import fnmatch
import mmap
import subprocess
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class LRUCache:
    """Simple Least Recently Used (LRU) cache for file contents.

    Attributes:
        cache: Dictionary storing cached data.
        maxsize: Maximum number of items the cache can hold.
    """

    def __init__(self, maxsize: int = 256):
        """Initializes the LRUCache.

        Args:
            maxsize: Maximum size of the cache. Defaults to 256.
        """
        self.cache = {}
        self.maxsize = maxsize

    def get(self, key: str) -> Any:
        """Retrieves an item from the cache.

        Args:
            key: The key to look up.

        Returns:
            The cached value if found, otherwise None.
        """
        return self.cache.get(key)

    def set(self, key: str, value: Any):
        """Adds or updates an item in the cache.

        Args:
            key: The key identifying the item.
            value: The value to store.
        """
        if len(self.cache) > self.maxsize:
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value

    def clear(self):
        """Removes all items from the cache."""
        self.cache.clear()


# Global cache instance for performance optimization across modules
file_cache = LRUCache()


def read_file_fast(path: pathlib.Path) -> str:
    """Reads file content efficiently using memory mapping and caching.

    Args:
        path: Path to the file to read.

    Returns:
        The file content as a string, or an empty string if reading fails.
    """
    cache_key = str(path)
    cached = file_cache.get(cache_key)
    if cached:
        return cached

    try:
        with open(path, "rb") as f:
            file_size = path.stat().st_size

            # Use memory mapping for large files (> 1MB) to optimize performance
            if file_size > 1024 * 1024:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    content = mm.read().decode("utf-8-sig", errors="replace")
            else:
                # Direct read for small files
                content = f.read().decode("utf-8-sig", errors="replace")

            # Cache result for future lookups
            file_cache.set(cache_key, content)
            return content

    except Exception as e:
        logger.warning(f"⚠️ Error reading {path}: {e}")
        return ""


def load_exclusion_patterns(
    project_path: pathlib.Path, extra_patterns: List[str] = None
) -> List[str]:
    """Loads file exclusion patterns from .analyzerignore or returns defaults.

    Args:
        project_path: Root directory of the project.
        extra_patterns: Additional patterns provided via CLI or config.

    Returns:
        A list of glob-style exclusion patterns.
    """
    patterns = []

    # 1. Priority: .analyzerignore (custom project configuration)
    ignore_file = project_path / ".analyzerignore"
    if ignore_file.exists():
        try:
            with open(ignore_file, encoding="utf-8") as f:
                patterns = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
        except Exception:
            pass

    # 2. Defaults if no ignore file is found
    if not patterns:
        patterns = [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "env",
            ".tox",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "build",
            "dist",
            "*.egg-info",
        ]

    if extra_patterns:
        patterns.extend(extra_patterns)

    return patterns


def is_test_file(path: pathlib.Path) -> bool:
    """Heuristically determines if a given file is a test file.

    Args:
        path: Path to the file to check.

    Returns:
        True if the file matches common test naming patterns or directory structures.
    """
    filename = path.name.lower()
    test_patterns = ["test_", "_test", "spec_", "_spec", "conftest"]

    return (
        any(pattern in filename for pattern in test_patterns)
        or "tests" in str(path).lower()
        or "test" in path.parent.name.lower()
    )


def count_test_files(project_path: pathlib.Path, exclusion_patterns: List[str]) -> int:
    """Counts non-excluded test files in the project.

    Args:
        project_path: Root directory to search.
        exclusion_patterns: List of patterns to ignore.

    Returns:
        The total count of identified test files.
    """
    count = 0
    for py_file in project_path.rglob("*.py"):
        rel_path = str(py_file.relative_to(project_path))
        if _matches_exclusion_pattern(py_file, rel_path, exclusion_patterns):
            continue
        if is_test_file(py_file):
            count += 1
    return count


def get_python_files_filtered(
    project_path: pathlib.Path, exclusion_patterns: List[str]
) -> List[pathlib.Path]:
    """Retrieves a sorted list of Python modules, excluding specific patterns and tests.

    Args:
        project_path: Root directory to search.
        exclusion_patterns: List of patterns to ignore.

    Returns:
        A sorted list of pathlib.Path objects for relevant Python files.
    """
    python_files = []

    for py_file in project_path.rglob("*.py"):
        rel_path = str(py_file.relative_to(project_path))

        if _matches_exclusion_pattern(py_file, rel_path, exclusion_patterns):
            continue

        if is_test_file(py_file):
            continue

        python_files.append(py_file)

    return sorted(python_files)


def _matches_exclusion_pattern(
    py_file: pathlib.Path, rel_path: str, patterns: List[str]
) -> bool:
    """Checks if a file or its path matches any exclusion patterns.

    Args:
        py_file: Full path to the file.
        rel_path: Path relative to project root.
        patterns: List of glob-style patterns to check.

    Returns:
        True if a match is found, False otherwise.
    """
    for pattern in patterns:
        if pattern.endswith("/"):
            pattern = pattern[:-1]

        if (
            fnmatch.fnmatch(rel_path, pattern)
            or fnmatch.fnmatch(py_file.name, pattern)
            or any(fnmatch.fnmatch(part, pattern) for part in py_file.parts)
        ):
            return True
    return False


def generate_tree_optimized(project_path: pathlib.Path) -> str:
    """Generates a text-based directory structure visualization.

    Attempts to use the system 'tree' command for accuracy and speed,
    falling back to a custom Python implementation if not available.

    Args:
        project_path: Directory to process.

    Returns:
        A string representing the directory tree.
    """
    try:
        result = subprocess.run(
            [
                "tree",
                "-I",
                "__pycache__|*.pyc|*.pyo|*.pycache|.git|.venv|venv|env",
                "-a",
                "--noreport",
                "-L",
                "4",
            ],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0:
            return result.stdout[:1500]
    except Exception:
        pass

    return _generate_tree_fallback(project_path)


def _generate_tree_fallback(
    project_path: pathlib.Path, max_depth: int = 4, max_files_per_dir: int = 8
) -> str:
    """Custom Python generator for directory structures when 'tree' is missing.

    Args:
        project_path: Directory to process.
        max_depth: Reaching limit for recursive traversal. Defaults to 4.
        max_files_per_dir: Maximum number of files to show per directory. Defaults to 8.

    Returns:
        A string representing the directory tree.
    """
    tree_lines = ["./"]

    for root, dirs, files in os.walk(project_path):
        depth = root[len(str(project_path)) :].count(os.sep)
        if depth > max_depth:
            continue

        # Prune hidden/private directories to reduce noise
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]

        indent = "    " * depth
        rel_root = os.path.relpath(root, project_path)
        if rel_root != ".":
            tree_lines.append(f"{indent}{os.path.basename(root)}/")

        file_indent = "    " * (depth + 1)
        sorted_files = sorted(files)
        for i, file in enumerate(sorted_files[:max_files_per_dir]):
            line = _format_tree_line(
                file, i, len(files), max_files_per_dir, file_indent
            )
            if line:
                tree_lines.append(line)
                if "..." in line:
                    break

    return "\n".join(tree_lines)


def _format_tree_line(
    file: str, index: int, total: int, limit: int, indent: str
) -> str:
    """Formats a single file entry or ellipsis for the tree visualization.

    Args:
        file: Filename to display.
        index: Current file index.
        total: Total files in the directory.
        limit: Display limit for files.
        indent: Indentation string.

    Returns:
        A formatted string line.
    """
    if index == limit - 1 and total > limit:
        return f"{indent}... (+{total - limit} more)"
    return f"{indent}{file}"


def count_file_types(project_path: pathlib.Path) -> Dict[str, int]:
    """Scans the project and counts occurrences of common file extensions.

    Args:
        project_path: Root directory to scan.

    Returns:
        A dictionary mapping extensions (e.g., '.py') to their counts.
    """
    extensions = {}
    common_exts = {
        ".py",
        ".txt",
        ".md",
        ".json",
        ".yml",
        ".yaml",
        ".html",
        ".css",
        ".js",
        ".xml",
        ".csv",
        ".sql",
    }

    for file in project_path.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower()
            if ext in common_exts or ext:
                extensions[ext] = extensions.get(ext, 0) + 1

    return dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:20])


def calculate_size_stats(project_path: pathlib.Path) -> Dict[str, Any]:
    """Computes high-level size and count statistics for the project.

    Args:
        project_path: Root directory to analyze.

    Returns:
        A dictionary with total size, file counts, and Python-specific metrics.
    """
    stats = _accumulate_directory_stats(project_path)

    total_files = stats["total_files"]
    total_size = stats["total_size"]
    python_size = stats["python_size"]

    return {
        "total_files": total_files,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "python_files": stats["python_files"],
        "python_size_mb": round(python_size / (1024 * 1024), 2),
        "avg_file_size_kb": (
            round(total_size / total_files / 1024, 2) if total_files > 0 else 0
        ),
        "python_percentage": (
            round(python_size / total_size * 100, 2) if total_size > 0 else 0
        ),
    }


def _accumulate_directory_stats(project_path: pathlib.Path) -> Dict[str, int]:
    """Traverses the project to collect raw size and count data.

    Args:
        project_path: Root directory to traverse.

    Returns:
        A dictionary with accumulated totals for files and sizes.
    """
    stats = {"total_files": 0, "total_size": 0, "python_files": 0, "python_size": 0}

    for entry in os.scandir(project_path):
        if entry.is_file():
            _process_entry(entry.name, entry.stat().st_size, stats)
        elif entry.is_dir() and not entry.name.startswith("."):
            for root, _, files in os.walk(entry.path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        _process_entry(file, size, stats)
                    except Exception:
                        pass
    return stats


def _process_entry(filename: str, size: int, stats: Dict[str, int]):
    """Updates a stats dictionary with data from a single file.

    Args:
        filename: Name of the file.
        size: Size of the file in bytes.
        stats: The statistics dictionary to update in-place.
    """
    stats["total_files"] += 1
    stats["total_size"] += size
    if filename.endswith(".py"):
        stats["python_files"] += 1
        stats["python_size"] += size


def analyze_structure(project_path: pathlib.Path, modules_count: int) -> Dict[str, Any]:
    """Generates a summary of project structure, types, and sizes.

    Args:
        project_path: Root directory to analyze.
        modules_count: Pre-calculated count of project modules.

    Returns:
        A dictionary consolidating tree visualization and structural stats.
    """
    return {
        "tree": generate_tree_optimized(project_path),
        "modules_count": modules_count,
        "file_types": count_file_types(project_path),
        "size_stats": calculate_size_stats(project_path),
    }
