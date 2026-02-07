"""Project scanning logic."""

import os
import pathlib
from typing import List, Dict, Any, NamedTuple
from .ignore_filter import IgnoreFilter


class ProjectScanResult(NamedTuple):
    """Encapsulates the results of a project-wide filesystem scan."""

    python_files: List[pathlib.Path]
    test_files_count: int
    file_types: Dict[str, int]
    size_stats: Dict[str, Any]


class ProjectScanner:
    """Consolidated project scanner that performs a single-pass traversal."""

    COMMON_EXTS = {
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

    def __init__(self, project_path: pathlib.Path, ignore_filter: IgnoreFilter):
        self.project_path = project_path
        self.ignore_filter = ignore_filter
        self.stats = {
            "total_files": 0,
            "total_size": 0,
            "python_files": 0,
            "python_size": 0,
        }
        self.file_types = {}
        self.python_files = []
        self.test_files_count = 0

    def scan(self) -> ProjectScanResult:
        for root, dirs, files in os.walk(self.project_path):
            rel_root = os.path.relpath(root, self.project_path)
            if rel_root == ".":
                rel_root = ""

            i = 0
            while i < len(dirs):
                d_path = pathlib.Path(root) / dirs[i]
                if self.ignore_filter.is_ignored(d_path):
                    del dirs[i]
                else:
                    i += 1

            for file in files:
                self._process_file(root, rel_root, file)

        return ProjectScanResult(
            python_files=sorted(self.python_files),
            test_files_count=self.test_files_count,
            file_types=dict(
                sorted(self.file_types.items(), key=lambda x: x[1], reverse=True)[:20]
            ),
            size_stats=self._finalize_stats(),
        )

    def _process_file(self, root: str, rel_root: str, file: str):
        file_path = os.path.join(root, file)
        path_obj = pathlib.Path(file_path)
        if self.ignore_filter.is_ignored(path_obj):
            return

        size = 0
        try:
            size = os.path.getsize(file_path)
        except OSError:
            pass

        self.stats["total_files"] += 1
        self.stats["total_size"] += size

        ext = os.path.splitext(file)[1].lower()
        if ext in self.COMMON_EXTS or ext:
            self.file_types[ext] = self.file_types.get(ext, 0) + 1

        if ext == ".py":
            self.stats["python_files"] += 1
            self.stats["python_size"] += size
            from .fs_helpers import is_test_file

            # DEBUG:
            ignored = is_test_file(path_obj)
            print(f"Scanner: {file_path}, is_test={ignored}")
            if ignored:
                self.test_files_count += 1
            else:
                self.python_files.append(path_obj)

    def _finalize_stats(self) -> Dict[str, Any]:
        ts = self.stats["total_size"]
        ps = self.stats["python_size"]
        tf = self.stats["total_files"]
        return {
            "total_files": tf,
            "total_size_mb": round(ts / (1024 * 1024), 2),
            "python_files": self.stats["python_files"],
            "python_size_mb": round(ps / (1024 * 1024), 2),
            "avg_file_size_kb": round(ts / tf / 1024, 2) if tf > 0 else 0,
            "python_percentage": round(ps / ts * 100, 2) if ts > 0 else 0,
        }


def scan_project(project_path: pathlib.Path, patterns: List[str]) -> ProjectScanResult:
    filt = IgnoreFilter(project_path, extra_patterns=patterns)
    scanner = ProjectScanner(project_path, filt)
    return scanner.scan()
