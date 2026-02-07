"""Aggregator components package."""

from .qgis import aggregate_qgis_compliance
from .formatter import format_complexity_agg

__all__ = ["aggregate_qgis_compliance", "format_complexity_agg"]
