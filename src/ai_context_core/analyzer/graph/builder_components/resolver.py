"""Logic for resolving import strings to project file paths."""

from typing import Dict, Optional


def resolve_import(imp: str, import_map: Dict[str, str]) -> Optional[str]:
    """Resolve an import string to a project file path.

    Args:
        imp: Import string (e.g., 'pkg.mod').
        import_map: Mapping of importable paths to file paths.

    Returns:
        Resolved file path or None.
    """
    if imp in import_map:
        return import_map[imp]

    if "." in imp:
        parts = imp.split(".")
        for i in range(len(parts), 0, -1):
            prefix = ".".join(parts[:i])
            if prefix in import_map:
                return import_map[prefix]
    return None
