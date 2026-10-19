"""Context fingerprinting and staleness primitives.

Each rendered artifact records a ``content_hash`` of the analyzed Python inputs
(relative path + file hash) and a ``render_fingerprint`` covering every render
input: the source hash, the effective configuration, embedded context documents
and the tool version. The freshness policy lives in :mod:`freshness`.
"""

import hashlib
import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

from .. import __version__
from ..analyzer.providers import context_fields, fs_utils
from ..analyzer.providers.fs_cache import compute_config_fingerprint

logger = logging.getLogger(__name__)

AI_CONTEXT = "AI_CONTEXT.md"
PROJECT_CONTEXT = "project_context.json"
MANIFEST = "context_manifest.json"
SYMBOLS = "symbols.json"
TRACKED_ARTIFACTS = (AI_CONTEXT, PROJECT_CONTEXT, MANIFEST)

HASH_PREFIX = "sha256:"


def compute_content_hash(
    project_path: pathlib.Path, exclusion_patterns: Optional[List[str]] = None
) -> str:
    """Hash the analyzed Python inputs (relative path + file content hash).

    Args:
        project_path: Project root.
        exclusion_patterns: Extra ignore patterns; resolved from the project when
            omitted.

    Returns:
        A ``sha256:<hex>`` string, stable across runs for unchanged inputs.
    """
    project_path = pathlib.Path(project_path).resolve()
    if exclusion_patterns is None:
        exclusion_patterns = fs_utils.load_exclusion_patterns(project_path, None)

    scan = fs_utils.scan_project(project_path, exclusion_patterns)
    return hash_files(project_path, scan.python_files)


def hash_files(project_path: pathlib.Path, files: List[pathlib.Path]) -> str:
    """Hash a pre-scanned list of files (relative path + content hash).

    Lets callers that already scanned the project avoid a redundant walk.

    Args:
        project_path: Project root.
        files: Files to include in the hash.

    Returns:
        A ``sha256:<hex>`` string.
    """
    project_path = pathlib.Path(project_path).resolve()
    entries: List[List[str]] = []
    for file_path in files:
        try:
            rel = str(pathlib.Path(file_path).relative_to(project_path))
            entries.append([rel, _hash_file(file_path)])
        except (OSError, ValueError) as e:  # pragma: no cover - unreadable file
            logger.warning("Skipping %s during hashing: %s", file_path, e)
    entries.sort()

    payload = json.dumps(entries, separators=(",", ":")).encode("utf-8")
    return HASH_PREFIX + hashlib.sha256(payload).hexdigest()


def _hash_file(path: pathlib.Path) -> str:
    """Hash file bytes directly (bypasses the process-global read cache)."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _doc_key(project_path: pathlib.Path, path: pathlib.Path) -> str:
    """Return a stable, project-relative key for an embedded document."""
    try:
        return str(path.relative_to(project_path))
    except ValueError:
        return str(path)


def _hash_context_docs(
    project_path: pathlib.Path,
    config: Dict[str, Any],
    include_md: Optional[List[str]] = None,
) -> List[List[str]]:
    """Hash every markdown file embedded as manual architecture notes."""
    entries: List[List[str]] = []
    for doc in context_fields.context_doc_paths(project_path, config, include_md):
        key = _doc_key(project_path, doc)
        try:
            digest = _hash_file(doc)
        except OSError:
            digest = "missing"
        entries.append([key, digest])
    entries.sort()
    return entries


def compute_render_fingerprint(
    project_path: pathlib.Path,
    config: Optional[Dict[str, Any]],
    content_hash: str,
    include_md: Optional[List[str]] = None,
) -> str:
    """Hash every input that can change a rendered artifact.

    Args:
        project_path: Project root.
        config: Effective configuration used for rendering.
        content_hash: Hash of the analyzed Python sources.
        include_md: Extra markdown globs supplied at render time.

    Returns:
        A ``sha256:<hex>`` string covering sources, configuration, embedded
        documents and the tool version.
    """
    project_path = pathlib.Path(project_path).resolve()
    config = config or {}
    payload = {
        "version": __version__,
        "content_hash": content_hash,
        "config_hash": compute_config_fingerprint(config) if config else None,
        "docs": _hash_context_docs(project_path, config, include_md),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return HASH_PREFIX + hashlib.sha256(encoded).hexdigest()


def read_recorded_meta(project_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Read the recorded ``_meta`` block from the manifest or context JSON."""
    project_path = pathlib.Path(project_path)
    for name in (MANIFEST, PROJECT_CONTEXT):
        data = _read_json(project_path / name)
        meta = (data or {}).get("_meta")
        if isinstance(meta, dict) and meta.get("content_hash"):
            return meta
    return None


def read_recorded_hash(project_path: pathlib.Path) -> Optional[str]:
    """Read the recorded ``content_hash`` from the manifest or context JSON."""
    meta = read_recorded_meta(project_path)
    return (meta or {}).get("content_hash")


def _symbols_report(
    project_path: pathlib.Path,
    current_hash: str,
    recorded_meta: Optional[Dict[str, Any]],
    missing: List[str],
) -> Dict[str, Any]:
    """Check ``symbols.json`` presence and freshness.

    A missing symbol index is only an error when it existed at render time.
    A present index without a source hash (pre-5.1.1 files) is reported as stale
    so it can be regenerated with ``ai-ctx symbols``.
    """
    path = project_path / SYMBOLS
    info: Dict[str, Any] = {"present": path.exists(), "fresh": None, "reason": ""}

    recorded_present = bool((recorded_meta or {}).get("symbols_present"))
    if recorded_present and not path.exists():
        missing.append(SYMBOLS)
        info["fresh"] = False
        info["reason"] = "symbols.json was present at render time but is missing"
        return info

    if not path.exists():
        return info

    data = _read_json(path) or {}
    recorded_symbols_hash = (data.get("_meta") or {}).get("content_hash")
    if not recorded_symbols_hash:
        info["fresh"] = False
        info["reason"] = "symbols.json has no content hash (run 'ai-ctx symbols')"
    elif recorded_symbols_hash != current_hash:
        info["fresh"] = False
        info["reason"] = "symbols.json is stale relative to the sources"
    else:
        info["fresh"] = True
    return info


def verify_context(project_path: pathlib.Path) -> Dict[str, Any]:
    """Verify that context artifacts are fresh relative to the current inputs.

    Thin compatibility wrapper over :func:`ai_context_core.context.freshness.verify_context`.

    Args:
        project_path: Project root.

    Returns:
        The freshness report.
    """
    from .freshness import verify_context as _verify_context

    return _verify_context(project_path)


def _read_json(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file, returning ``None`` on absence or error."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        logger.warning("Could not read %s: %s", path, e)
        return None
