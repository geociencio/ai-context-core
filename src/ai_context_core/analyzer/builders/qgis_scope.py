"""Glob-path helpers for scoping QGIS i18n analysis."""

from typing import Dict, Any, Pattern
import re
import fnmatch
import logging

logger = logging.getLogger(__name__)

_PATTERN_CACHE: Dict[str, Pattern[str]] = {}


def _match_path(path: str, pattern: str) -> bool:
    """Helper to match path against glob pattern robustly using regex and caching.

    Supports recursive ** patterns globally on all Python versions (3.9+).
    """
    # Normalize paths to use forward slashes for consistency
    path = path.replace("\\", "/")
    pattern = pattern.replace("\\", "/")

    if pattern not in _PATTERN_CACHE:
        try:
            if "**" not in pattern:
                # Standard glob behavior for non-recursive patterns
                _PATTERN_CACHE[pattern] = re.compile(fnmatch.translate(pattern))
            else:
                # Convert recursive glob to regex
                # 1. Escape everything
                # 2. Replace escaped **/ with (.*/)? (matches zero or more directories)
                # 3. Replace escaped * with [^/]* (matches within one directory)
                regex_str = (
                    re.escape(pattern)
                    .replace(r"\*\*/", "(.*/)?")
                    .replace(r"\*", "[^/]*")
                )

                # Ensure it matches as a suffix if it doesn't start with a slash/glob
                if not regex_str.startswith("(\\.\\*/)?") and not pattern.startswith(
                    "/"
                ):
                    regex_str = f"^(.*/)?{regex_str}$"
                else:
                    regex_str = f"^{regex_str}$"

                _PATTERN_CACHE[pattern] = re.compile(regex_str)
        except Exception as exc:
            # Fallback if regex generation fails, but never silently
            logger.warning("Invalid glob pattern %r: %s", pattern, exc)
            return False

    regex = _PATTERN_CACHE[pattern]
    return bool(regex.match(path))


def _should_include_for_i18n(
    module_data: Dict[str, Any], i18n_config: Dict[str, Any], scope: str
) -> bool:
    """Check if a module should be included in i18n analysis based on scope.

    Args:
        module_data: Individual module analysis result.
        i18n_config: i18n configuration with scope and patterns.
        scope: Resolved i18n scope (``all``, ``gui_only`` or ``custom``).

    Returns:
        True if the module must be counted for i18n coverage.
    """
    if scope == "all":
        return True

    module_path = module_data.get("path", "")
    if not module_path:
        return True  # Include if no path info

    if scope == "gui_only":
        patterns = i18n_config.get(
            "gui_patterns",
            ["gui/**/*.py", "dialogs/**/*.py", "widgets/**/*.py", "ui/**/*.py"],
        )
    elif scope == "custom":
        patterns = i18n_config.get("include_patterns", [])
        exclude_patterns = i18n_config.get("exclude_patterns", [])

        # Check exclusions first
        for pattern in exclude_patterns:
            if _match_path(module_path, pattern):
                return False
    else:
        return True  # Unknown scope, include all

    # Check inclusions
    for pattern in patterns:
        if _match_path(module_path, pattern):
            return True

    return False
