"""Compatibility facade for dependency classifier."""

from ..builders.classifier import classify_imports

# Legacy alias
classify_import = classify_imports

__all__ = ["classify_import", "classify_imports"]
