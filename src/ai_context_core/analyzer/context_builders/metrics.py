"""Builders for metrics and complexity sections."""

from .base import BaseContextBuilder
from typing import List

class MetricsBuilder(BaseContextBuilder):
    """Adds metrics and complexity sections."""

    def build(self, lines: List[str]) -> None:
        c = self.analyses.get("complexity", {})
        m = self.analyses.get("metrics", {})
        
        lines.append("\n## 📈 COMPLEXITY AND METRICS")
        lines.append(f"- **Total Modules**: {c.get('total_modules', 0)}")
        lines.append(f"- **Source Lines (SLOC)**: {c.get('total_lines', 0):,}")
        lines.append(
            f"- **Total Physical Lines**: {c.get('total_physical_lines', 0) or m.get('total_physical_lines', 0):,}"
        )
        lines.append(f"- **Functions**: {c.get('total_functions', 0)}")
        lines.append(f"- **Classes**: {c.get('total_classes', 0)}")
        lines.append(f"- **Average Complexity**: {c.get('average_complexity', 0):.1f}")
        lines.append(
            f"- **Avg Maintenance Index**: {c.get('avg_maintenance_index', 0) or m.get('avg_maintenance_index', 0):.1f}"
        )

        cm = [mod[0] for mod in c.get("most_complex_modules", [])[:3]]
        lines.append(f"- **Most Complex Modules**: {', '.join(cm)}")
