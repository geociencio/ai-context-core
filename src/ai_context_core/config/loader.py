"""Deprecated configuration loading facade.

Retained for backward compatibility. New code should import ``load_config``
from ``ai_context_core.analyzer.providers.config_loader`` instead.
"""

import pathlib
import warnings
from typing import Any, Dict, Optional

from ai_context_core.analyzer.providers.config_loader import load_config as _load_config


class ConfigLoader:
    """Deprecated facade delegating to the canonical configuration loader.

    Attributes:
        base_path: Absolute directory containing this module.
        profiles_path: Directory containing named profiles (informational only).
    """

    def __init__(self) -> None:
        """Initializes the facade with standard project paths."""
        self.base_path = pathlib.Path(__file__).parent
        self.profiles_path = self.base_path / "profiles"

    def load_config(
        self, profile_name: Optional[str] = None, override_config: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Load configuration by delegating to the canonical loader.

        Args:
            profile_name: Optional profile name (e.g. ``"qgis"``).
            override_config: Optional final overrides.

        Returns:
            The merged configuration dictionary.
        """
        warnings.warn(
            "ConfigLoader is deprecated; use "
            "ai_context_core.analyzer.providers.config_loader.load_config instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _load_config(
            root_path=None, profile_name=profile_name, override_config=override_config
        )


def list_profiles() -> list[str]:
    """Retrieves a list of all available configuration profile names.

    Returns:
        A list of profile stem names (e.g. ``['generic', 'qgis']``).
    """
    profiles_dir = pathlib.Path(__file__).parent / "profiles"
    profiles = ["generic"]
    if not profiles_dir.exists():
        return profiles

    profiles.extend(p.stem for p in profiles_dir.glob("*.yaml"))
    profiles.extend(p.stem for p in profiles_dir.glob("*.toml"))

    return sorted(list(set(profiles)))
