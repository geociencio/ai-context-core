"""Unused-import aggregation with package re-export exemptions."""

from typing import Any, Dict, List, Optional


def ignore_package_reexports(config: Optional[Dict[str, Any]]) -> bool:
    """Return whether ``__init__.py`` re-exports should be exempted.

    Args:
        config: Effective analysis configuration.

    Returns:
        True (the default) when unused-import findings for package
        ``__init__.py`` files should be dropped, since those imports usually
        re-export the public API.
    """
    if not isinstance(config, dict):
        return True
    patterns = config.get("patterns") or {}
    unused_cfg = patterns.get("unused_imports") or {}
    return bool(unused_cfg.get("ignore_package_reexports", True))


def detect_unused_imports_in_project(
    modules_data: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, List[str]]:
    """Collects unused imports across all modules.

    Args:
        modules_data: Per-module analysis results.
        config: Optional configuration controlling re-export exemptions.

    Returns:
        Mapping of ``module_path -> list_of_unused_imports``.
    """
    skip_reexports = ignore_package_reexports(config)
    unused: Dict[str, List[str]] = {}
    for mod in modules_data:
        if not mod.get("unused_imports"):
            continue
        if skip_reexports and str(mod.get("path", "")).endswith("__init__.py"):
            continue
        unused[mod["path"]] = mod["unused_imports"]
    return unused
