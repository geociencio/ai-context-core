"""QGIS specific compliance and pattern detection.

This module is a facade that re-exports functionality from ast_qgis_components.
"""

from .qgis_visitor import GenericQGISComplianceVisitor
from .logic import is_qgis_entry_point_node, check_qgis_compliance

from ..registry import register_detector


@register_detector("qgis_compliance")
def check_qgis_compliance_registered(tree):
    """Registered QGIS compliance check."""
    return check_qgis_compliance(tree)


__all__ = [
    "GenericQGISComplianceVisitor",
    "is_qgis_entry_point_node",
    "check_qgis_compliance",
    "check_qgis_compliance_registered",
]

# Alias for backward compatibility
QGISComplianceVisitor = GenericQGISComplianceVisitor
