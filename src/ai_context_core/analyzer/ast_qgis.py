"""QGIS specific compliance and pattern detection.

This module is a facade that re-exports functionality from ast_qgis_components.
"""

from .ast_qgis_components import (
    GenericQGISComplianceVisitor,
    is_qgis_entry_point_node,
    check_qgis_compliance,
)

__all__ = [
    "GenericQGISComplianceVisitor",
    "is_qgis_entry_point_node",
    "check_qgis_compliance",
]

# Alias for backward compatibility
QGISComplianceVisitor = GenericQGISComplianceVisitor
