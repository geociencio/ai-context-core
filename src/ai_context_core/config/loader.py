"""Configuration helpers.

Configuration loading is canonical in
``ai_context_core.analyzer.providers.config_loader.load_config``. This module
only exposes profile discovery.
"""

import pathlib


def list_profiles() -> list[str]:
    """Retrieve the list of available configuration profile names.

    Returns:
        Sorted profile stem names; always includes ``"generic"``.
    """
    profiles_dir = pathlib.Path(__file__).parent / "profiles"
    profiles = ["generic"]
    if not profiles_dir.exists():
        return profiles

    profiles.extend(p.stem for p in profiles_dir.glob("*.yaml"))
    profiles.extend(p.stem for p in profiles_dir.glob("*.toml"))

    return sorted(set(profiles))
