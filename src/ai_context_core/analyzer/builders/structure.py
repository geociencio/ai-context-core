"""Builders for structure, entry points, and manual notes."""

from .context_base import BaseContextBuilder
from typing import List


class StructureBuilder(BaseContextBuilder):
    """Adds project structure and entry points."""

    def build(self, lines: List[str]) -> None:
        s = self.analyses.get("structure", {})
        lines.append("## 📁 PROJECT STRUCTURE")
        lines.append(f"\n{s.get('tree', 'N/A')[:1200]}\n")

        ep = self.analyses.get("entry_points", [])
        lines.append("## 🎯 ENTRY POINTS")
        for item in ep[:10]:
            if isinstance(item, dict):
                path = item.get("path", "N/A")
                etype = item.get("type") or "unknown"
                lines.append(f"- `{path}` ({etype})")
            else:
                lines.append(f"- `{item}`")
        if len(ep) > 10:
            lines.append(f"... and {len(ep) - 10} more")

        notes = self.analyses.get("manual_notes", "")
        if notes:
            lines.append("\n## 📝 MANUAL ARCHITECTURE NOTES")
            lines.append(notes)
