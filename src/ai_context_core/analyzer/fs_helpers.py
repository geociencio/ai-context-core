"""Miscellaneous filesystem helpers."""

import mmap
import pathlib
import hashlib
from typing import List
from .ignore_filter import IgnoreFilter

def read_file_fast(path: pathlib.Path) -> str:
    from .fs_cache import file_cache
    cache_key = str(path)
    cached = file_cache.get(cache_key)
    if cached:
        return cached
    try:
        if not path.exists():
            return ""
        with open(path, "rb") as f:
            file_size = path.stat().st_size
            if file_size > 1024 * 1024:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    content = mm.read().decode("utf-8-sig", errors="replace")
            else:
                content = f.read().decode("utf-8-sig", errors="replace")
            file_cache.set(cache_key, content)
            return content
    except Exception:
        return ""

def is_test_file(path: pathlib.Path) -> bool:
    filename = path.name.lower()
    test_patterns = ["test_", "_test", "spec_", "_spec", "conftest"]
    return (
        any(pattern in filename for pattern in test_patterns)
        or "tests" in str(path).lower()
        or "test" in path.parent.name.lower()
    )

def calculate_file_hash(path: pathlib.Path) -> str:
    try:
        content = read_file_fast(path)
        if not content:
            return ""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    except Exception:
        return ""

def load_exclusion_patterns(project_path: pathlib.Path, extra: List[str] = None) -> List[str]:
    return IgnoreFilter(project_path, extra).patterns
