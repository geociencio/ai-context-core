"""Canonical configuration loading logic for the analyzer engine.

This module is the single source of truth for merging analyzer configuration.
The legacy ``ai_context_core.config.loader.ConfigLoader`` facade delegates here.

Resolution order (later layers win):
    1. ``config/defaults.toml`` (fallback to hardcoded defaults).
    2. Named profile ``config/profiles/<name>.{toml,yaml}``.
    3. Project config ``<root>/.ai-context/config.toml`` (legacy ``config.yaml``
       fallback, deprecated).
    4. Explicit ``override_config`` (e.g. CLI flags).
"""

import logging
import pathlib
import warnings
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

_CONFIG_DIR = pathlib.Path(__file__).resolve().parents[2] / "config"


def load_config(
    root_path: Optional[pathlib.Path] = None,
    profile_name: Optional[str] = None,
    override_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Load analyzer configuration by merging defaults, profile, project, and overrides.

    Args:
        root_path: Project root. Project config is only read when not ``None``.
        profile_name: Optional profile name (e.g. ``"qgis"``). If not given, a
            ``profile_name`` key in the project config is honored.
        override_config: Optional final overrides (highest precedence).

    Returns:
        The merged configuration dictionary.
    """
    config = _load_defaults()
    project = _load_project_config(root_path) if root_path is not None else {}

    if profile_name is None and "profile_name" in project:
        profile_name = project.pop("profile_name")

    if profile_name:
        config = _merge_dicts(config, _load_profile(profile_name))

    if project:
        config = _merge_dicts(config, project)

    if override_config:
        config = _merge_dicts(config, override_config)

    return config


def _load_defaults() -> Dict[str, Any]:
    """Load ``config/defaults.toml``, falling back to hardcoded defaults."""
    return _read_file(_CONFIG_DIR / "defaults.toml") or _get_hardcoded_defaults()


def _load_profile(profile_name: str) -> Dict[str, Any]:
    """Load a named profile (TOML preferred, YAML legacy)."""
    config = _read_file(_CONFIG_DIR / "profiles" / f"{profile_name}.toml")
    if config:
        return config

    config = _read_file(_CONFIG_DIR / "profiles" / f"{profile_name}.yaml")
    if config:
        return config

    logger.warning("Profile '%s' not found; using defaults.", profile_name)
    return {}


def _load_project_config(root_path: pathlib.Path) -> Dict[str, Any]:
    """Load project config (``config.toml`` preferred, ``config.yaml`` legacy)."""
    config = _read_file(root_path / ".ai-context" / "config.toml")
    if config:
        return config

    yaml_path = root_path / ".ai-context" / "config.yaml"
    if yaml_path.exists():
        warnings.warn(
            ".ai-context/config.yaml is deprecated; migrate to config.toml.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _read_file(yaml_path)

    return {}


def _read_file(path: pathlib.Path) -> Dict[str, Any]:
    """Load a TOML or YAML config file, returning ``{}`` on any error."""
    if not path.exists():
        return {}

    try:
        if path.suffix == ".toml":
            if tomllib is None:
                return {}
            with open(path, "rb") as f:
                return tomllib.load(f) or {}
        if path.suffix == ".yaml":
            import yaml

            return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        logger.warning("Failed to load config %s: %s", path, e)

    return {}


def _merge_dicts(base: Dict, update: Dict) -> Dict:
    """Recursively merge ``update`` into ``base``, returning the mutated ``base``."""
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dicts(base[key], value)
        else:
            base[key] = value
    return base


def _get_hardcoded_defaults() -> Dict[str, Any]:
    """Return fallback hardcoded configuration."""
    return {
        "quality_weights": {
            "docstrings": 30,
            "complexity_low": 20,
            "size_small": 15,
            "has_main": 5,
            "no_syntax_error": 30,
            "complexity_medium": 10,
            "complexity_high": -10,
            "size_medium": 10,
        },
        "thresholds": {
            "complexity_low": 5,
            "complexity_medium": 15,
            "complexity_high": 25,
            "size_small": 200,
            "size_medium": 500,
        },
        "scoring": {
            "base_score": 100.0,
            "complexity_medium_threshold": 15.0,
            "complexity_medium_penalty_per_point": 2.0,
            "complexity_high_threshold": 25.0,
            "complexity_high_penalty_per_point": 0.5,
            "complexity_high_penalty_cap": 10.0,
            "maintainability_threshold": 65.0,
            "maintainability_penalty_per_point": 1.5,
            "no_tests_penalty": 20.0,
            "tests_bonus_per_file": 2.0,
            "tests_bonus_cap": 10.0,
        },
    }
