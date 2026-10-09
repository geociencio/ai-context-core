"""Detection helpers for QGIS Processing framework usage."""

from typing import Any, Dict, List


def has_processing_imports(m_data: List[Dict[str, Any]]) -> bool:
    """Return True when any module imports the QGIS Processing framework.

    Args:
        m_data: Per-module analysis results.

    Returns:
        True if a module imports ``processing`` or references ``QgsProcessing*``,
        signalling an intent to use the Processing framework.
    """
    for mod in m_data:
        for imp in mod.get("imports", []):
            if imp == "processing" or imp.startswith("processing.") or "QgsProcessing" in imp:
                return True
    return False
