"""Dependency analysis components package."""

from .classifier import classify_imports
from .parser import parse_dependency_files

__all__ = ["classify_imports", "parse_dependency_files"]
