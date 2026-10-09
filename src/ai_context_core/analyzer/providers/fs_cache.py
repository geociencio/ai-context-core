"""File content and analysis cache management."""

import hashlib
import json
import pathlib
from collections import OrderedDict
from typing import Dict, Any, Optional

from ai_context_core import __version__

CACHE_SCHEMA = 1
_CACHE_FILENAME = ".ai_context_cache.json"


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


def compute_config_fingerprint(config: Optional[Dict[str, Any]]) -> str:
    """Compute a stable fingerprint for the effective analysis configuration.

    Args:
        config: The effective analysis configuration dictionary.

    Returns:
        A short, deterministic hex digest used to invalidate the cache whenever
        the configuration changes.
    """
    try:
        payload = json.dumps(config or {}, sort_keys=True, default=str)
    except (TypeError, ValueError):
        payload = repr(config)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_cache(
    project_path: pathlib.Path, config_fingerprint: Optional[str] = None
) -> Dict[str, Any]:
    """Load the analysis cache, rejecting entries from another tool version.

    The cache is only reused when its ``_meta`` block matches the current
    ``CACHE_SCHEMA``, package version, and configuration fingerprint. Otherwise
    the cache is treated as empty so stale results are never replayed.

    Args:
        project_path: Root directory of the analyzed project.
        config_fingerprint: Fingerprint of the effective configuration.

    Returns:
        A mapping of ``relative_path -> entry`` for compatible caches, or an
        empty dict when the cache is missing, corrupt, or stale.
    """
    cache_file = project_path / _CACHE_FILENAME
    if not cache_file.exists():
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    meta = data.get("_meta", {})
    if (
        meta.get("schema") != CACHE_SCHEMA
        or meta.get("version") != __version__
        or meta.get("config_fingerprint") != config_fingerprint
    ):
        return {}
    return {k: v for k, v in data.items() if k != "_meta"}


def save_cache(
    project_path: pathlib.Path,
    cache_data: Dict[str, Any],
    config_fingerprint: Optional[str] = None,
) -> None:
    """Persist the analysis cache together with its version metadata.

    Args:
        project_path: Root directory of the analyzed project.
        cache_data: Mapping of ``relative_path -> entry`` to persist.
        config_fingerprint: Fingerprint of the effective configuration.
    """
    cache_file = project_path / _CACHE_FILENAME
    payload: Dict[str, Any] = {
        "_meta": {
            "schema": CACHE_SCHEMA,
            "version": __version__,
            "config_fingerprint": config_fingerprint,
        }
    }
    payload.update({k: v for k, v in cache_data.items() if k != "_meta"})
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
