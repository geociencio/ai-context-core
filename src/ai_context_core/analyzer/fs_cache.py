"""File content and analysis cache management."""

import json
import pathlib
from collections import OrderedDict
from typing import Dict, Any


class LRUCache:
    def __init__(self, maxsize: int = 256):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key: str) -> Any:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()


file_cache = LRUCache()


def load_cache(project_path: pathlib.Path) -> Dict[str, Any]:
    cache_file = project_path / ".ai_context_cache.json"
    if not cache_file.exists():
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(project_path: pathlib.Path, cache_data: Dict[str, Any]):
    cache_file = project_path / ".ai_context_cache.json"
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
