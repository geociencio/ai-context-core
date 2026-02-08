"""Logic for resolving file paths and import strings for the import graph."""

from typing import Dict, Optional


def get_importable_path(path: str) -> Optional[str]:
    """Map a file path to an importable python path (e.g., 'pkg.mod').

    Args:
        path: Relative file path.

    Returns:
        The importable python path or None.
    """
    clean_path = path.replace("\\", "/")
    if clean_path.startswith("src/"):
        clean_path = clean_path[4:]

    importable = clean_path.replace(".py", "").replace("/", ".")
    if importable.endswith(".__init__"):
        importable = importable[:-9]

    return importable


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
