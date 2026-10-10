"""Optimization opportunity detection for analysis modules.

Security scanning previously lived here; it moved to ``qgis-plugin-analyzer``
(v5.0.0 context-only contract). Only the optimization finder remains.
"""

from .optimizations import find_optimizations  # noqa: F401

__all__ = ["find_optimizations"]
