"""Compatibility facade for config loader."""

from ..providers.config_loader import load_config, _get_hardcoded_defaults

__all__ = ["load_config", "_get_hardcoded_defaults"]
