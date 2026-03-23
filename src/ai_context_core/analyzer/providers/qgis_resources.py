import os
import pathlib
import xml.etree.ElementTree as ET
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
        "plugin_xml": {},
        "resource_files": [],
        "issues": [],
    }

    # 1. Analyze metadata.txt (Standard QGIS 3+)
    metadata_txt = project_path / "metadata.txt"
    if metadata_txt.exists():
        results["metadata"] = _parse_metadata_txt(metadata_txt)

    # 2. Analyze plugin.xml (Legacy or specific distribution)
    plugin_xml_path = project_path / "plugin.xml"
    if plugin_xml_path.exists():
        results["plugin_xml"] = _parse_plugin_xml(plugin_xml_path)

    # 3. Check for inconsistencies
    if results["metadata"] and results["plugin_xml"]:
        _check_inconsistencies(
            results["metadata"], results["plugin_xml"], results["issues"]
        )

    # 4. Look for .qrc files
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


def _parse_plugin_xml(path: pathlib.Path) -> Dict[str, str]:
    """Parse QGIS plugin.xml file."""
    metadata = {}
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        # Common fields in plugin.xml
        for child in root:
            if child.text:
                metadata[child.tag] = child.text
    except Exception:
        pass
    return metadata


def _check_inconsistencies(
    meta_txt: Dict[str, str], meta_xml: Dict[str, str], issues: list
) -> None:
    """Check for name/version mismatches between metadata.txt and plugin.xml."""
    # Version check
    v_txt = meta_txt.get("version")
    v_xml = meta_xml.get("version")
    if v_txt and v_xml and v_txt != v_xml:
        issues.append(
            f"Version mismatch: metadata.txt ({v_txt}) vs plugin.xml ({v_xml})"
        )

    # Name check
    n_txt = meta_txt.get("name")
    n_xml = meta_xml.get("name")
    if n_txt and n_xml and n_txt != n_xml:
        issues.append(f"Name mismatch: metadata.txt ({n_txt}) vs plugin.xml ({n_xml})")
