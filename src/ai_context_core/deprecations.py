"""Deprecation helpers for legacy compatibility facades."""

import warnings

# Version in which deprecated compatibility paths are scheduled for removal.
REMOVAL_VERSION = "4.0.0"


def warn_deprecated(old_path: str, new_path: str) -> None:
    """Emit a DeprecationWarning for a legacy import path.

    Args:
        old_path: Deprecated module or attribute path.
        new_path: Canonical replacement path.
    """
    warnings.warn(
        f"{old_path} is deprecated and will be removed in v{REMOVAL_VERSION}; "
        f"use {new_path} instead.",
        DeprecationWarning,
        stacklevel=3,
    )
