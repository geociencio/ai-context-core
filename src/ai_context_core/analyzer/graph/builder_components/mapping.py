"""Logic for mapping file paths to importable python paths."""

from typing import Optional


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
