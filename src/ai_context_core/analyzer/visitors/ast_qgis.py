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


def __getattr__(name: str):
    """Warn on access to deprecated aliases (PEP 562)."""
    if name == "QGISComplianceVisitor":
        from ai_context_core.deprecations import warn_deprecated

        warn_deprecated(
            "ai_context_core.analyzer.visitors.ast_qgis.QGISComplianceVisitor",
            "ai_context_core.analyzer.visitors.qgis_visitor.GenericQGISComplianceVisitor",
        )
        return GenericQGISComplianceVisitor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
