"""Builders for patterns and anti-patterns sections."""

from .base import BaseContextBuilder
from typing import List


class PatternsBuilder(BaseContextBuilder):
    """Adds detected patterns and anti-patterns."""

    def build(self, lines: List[str]) -> None:
        pats = self.analyses.get("patterns", {})
        lines.append("\n## 🏗️ DETECTED PATTERNS")
        if not pats:
            lines.append("No clear design patterns detected.")
        else:
            for name, occs in pats.items():
                lines.append(f"### {name}")
                for o in occs[:3]:
                    lines.append(
                        f"- **{o.get('class') or o.get('name') or 'N/A'}** in `{o.get('module', 'N/A')}` ({o.get('confidence', 0)}%)"
                    )
                    for ev in o.get("evidence", []):
                        lines.append(f"  - _Evidence: {ev}_")

        ap = self.analyses.get("antipatterns", [])
        if ap:
            lines.append("\n## ⚠️ DETECTED ANTI-PATTERNS")
            for i in ap[:5]:
                lines.append(f"- **{i['module']}**")
                for issue in i.get("issues", [])[:2]:
                    lines.append(f"  - {issue.get('message', 'N/A')}")
