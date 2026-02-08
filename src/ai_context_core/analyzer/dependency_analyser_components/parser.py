"""Compatibility facade for dependency parser."""

from ..builders.parser import parse_dependency_files

# Legacy alias
parse_import_statement = parse_dependency_files

__all__ = ["parse_import_statement", "parse_dependency_files"]
