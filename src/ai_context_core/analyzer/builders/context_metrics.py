"""Builders for metrics and complexity sections."""

from .context_base import BaseContextBuilder
from . import metric_keys
from . import formatter
from typing import List


class MetricsBuilder(BaseContextBuilder):
    """Adds metrics and complexity sections."""

    def build(self, lines: List[str]) -> None:
        c = self.analyses.get("complexity", {})
        m = self.analyses.get("metrics", {})

        lines.append("\n## 📈 COMPLEXITY AND METRICS")
        lines.append(f"- **Total Modules**: {c.get(formatter.TOTAL_MODULES, 0)}")
        lines.append(f"- **Source Lines (SLOC)**: {c.get(formatter.TOTAL_LINES, 0):,}")
        lines.append(
            f"- **Total Physical Lines**: {c.get(formatter.TOTAL_PHYSICAL_LINES, 0) or m.get(metric_keys.TOTAL_PHYSICAL_LINES, 0):,}"
        )
        lines.append(f"- **Functions**: {c.get(formatter.TOTAL_FUNCTIONS, 0)}")
        lines.append(f"- **Classes**: {c.get(formatter.TOTAL_CLASSES, 0)}")
        lines.append(
            f"- **Avg Cyclomatic Complexity**: {c.get(formatter.AVERAGE_COMPLEXITY, 0):.1f}"
        )
        lines.append(
            f"- **Avg Maintenance Index**: {c.get(formatter.AVG_MAINTENANCE_INDEX, 0) or m.get(metric_keys.AVG_MAINTENANCE_INDEX, 0):.1f}"
        )

        cm = [mod[0] for mod in c.get(formatter.MOST_COMPLEX_MODULES, [])[:3]]
        lines.append(f"- **Most Complex Modules**: {', '.join(cm)}")
