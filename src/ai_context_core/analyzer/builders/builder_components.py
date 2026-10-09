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


def resolve_import(
    imp: str, import_map: Dict[str, str], top_level_names: Optional[set] = None
) -> Optional[str]:
    """Resolve an import string to a project file path.

    Args:
        imp: Import string (e.g., 'pkg.mod').
        import_map: Mapping of importable paths to file paths.
        top_level_names: Optional set of valid top-level package names. When
            given, a leading non-top-level segment (e.g. a distribution package
            prefix like ``sec_interp``) is stripped before resolving.

    Returns:
        Resolved file path or None.
    """
    if imp in import_map:
        return import_map[imp]

    parts = imp.split(".")
    # Longest trailing-prefix match (submodule imports resolve to their package).
    for i in range(len(parts), 0, -1):
        prefix = ".".join(parts[:i])
        if prefix in import_map:
            return import_map[prefix]

    # Strip a spurious top-level package prefix (e.g. 'sec_interp.core.x' where
    # only 'core.x' is importable) and resolve the remainder.
    if top_level_names:
        for i in range(1, len(parts)):
            if parts[i] not in top_level_names:
                continue
            suffix = ".".join(parts[i:])
            if suffix in import_map:
                return import_map[suffix]

    return None
