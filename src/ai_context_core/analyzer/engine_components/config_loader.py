"""Configuration loading logic for the analyzer engine."""

import logging
import pathlib
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

def load_config(root_path: pathlib.Path) -> Dict[str, Any]:
    """Load configuration from defaults.toml and optional project overrides."""
    default_config = {}
    if tomllib:
        try:
            defaults_path = pathlib.Path(__file__).parent.parent / ".." / "config" / "defaults.toml"
            if defaults_path.exists():
                with open(defaults_path, "rb") as f:
                    default_config = tomllib.load(f)
        except Exception as e:
            logger.warning(f"Failed to load defaults.toml: {e}")

    if not default_config:
        return _get_hardcoded_defaults()

    override_config = {}
    if tomllib:
        try:
            project_config_path = root_path / ".ai-context" / "config.toml"
            if project_config_path.exists():
                with open(project_config_path, "rb") as f:
                    override_config = tomllib.load(f)
        except Exception as e:
            logger.warning(f"Failed to load project config.toml: {e}")

    final_config = default_config.copy()
    for section, values in override_config.items():
        if isinstance(values, dict) and section in final_config:
            final_config[section].update(values)
        else:
            final_config[section] = values

    return final_config

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
    }
