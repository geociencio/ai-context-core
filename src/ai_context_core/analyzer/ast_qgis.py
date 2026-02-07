"""QGIS specific compliance and pattern detection."""

import ast
from typing import Dict, Any


from .ast_qgis_components import (
    GenericQGISComplianceVisitor as QGISComplianceVisitor,
    is_qgis_entry_point_node,
    check_qgis_compliance
)
