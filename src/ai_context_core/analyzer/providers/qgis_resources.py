"""QGIS resource analysis (plugin.xml, .qrc)."""

import os
import pathlib
from typing import Dict, Any


def analyze_qgis_resources(project_path: pathlib.Path) -> Dict[str, Any]:
    """Analyze non-Python QGIS resources like plugin.xml and .qrc files.

    Args:
        project_path: Path to the project root.

    Returns:
        Dictionary with findings from resource analysis.
    """
    results = {
        "metadata": {},
        "resource_files": [],
        "issues": [],
    }

    # 1. Analyze plugin.xml / metadata.txt
    # QGIS 3 plugins use metadata.txt as source of truth.

    # Let's check for metadata.txt first as it's the standard.
    metadata_txt = project_path / "metadata.txt"
    if metadata_txt.exists():
        results["metadata"] = _parse_metadata_txt(metadata_txt)

    # 2. Look for .qrc files
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".qrc"):
                results["resource_files"].append(
                    os.path.relpath(os.path.join(root, file), project_path)
                )

    return results


def _parse_metadata_txt(path: pathlib.Path) -> Dict[str, str]:
    """Parse standard QGIS metadata.txt file."""
    metadata = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.split("=", 1)
                    metadata[key.strip()] = value.strip()
    except Exception:
        pass
    return metadata
