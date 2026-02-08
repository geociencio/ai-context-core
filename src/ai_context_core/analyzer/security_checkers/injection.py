"""Compatibility facade for SQL injection checker."""

from ..visitors.injection import InjectionChecker

__all__ = ["InjectionChecker"]
