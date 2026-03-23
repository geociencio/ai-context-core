"""Builder for QGIS compliance section in AI context."""

from .context_base import BaseContextBuilder
from typing import List
from .aggregator_qgis import QGISSummarizer


class QGISBuilder(BaseContextBuilder):
    """Adds QGIS compliance analysis to AI Context documents."""

    def build(self, lines: List[str]) -> None:
        """Appends QGIS compliance summary to the markdown lines.

        Args:
            lines: List of markdown lines.
        """
        q = self.analyses.get("qgis_compliance", {})
        if not q:
            return

        # Show if it has QGIS content
        has_metadata = q.get("metadata", {}).get("exists", False)
        has_framework = q.get("processing_framework_detected", False)

        if not has_metadata and not has_framework:
            return

        lines.append("## 🗺️ QGIS STANDARDS COMPLIANCE")

        # Use existing summarizer logic
        summarizer = QGISSummarizer(self.analyses)
        lines.append(summarizer.build())
        lines.append("")
