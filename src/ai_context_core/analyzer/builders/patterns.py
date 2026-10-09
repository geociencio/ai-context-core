"""Builders for patterns and anti-patterns sections."""

from .context_base import BaseContextBuilder
from typing import List


class PatternsBuilder(BaseContextBuilder):
    """Adds detected patterns and anti-patterns."""

    def build(self, lines: List[str]) -> None:
        from ..visitors.antipattern_base import severity_rank

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
            for entry in ap:
                entry["issues"] = sorted(
                    entry["issues"],
                    key=lambda i: (severity_rank(i.get("severity", "low")), i.get("line", 0)),
                )
            ap = sorted(
                ap,
                key=lambda e: (
                    severity_rank(e["issues"][0].get("severity", "low")) if e["issues"] else 3,
                    e.get("module", ""),
                ),
            )
            lines.append("\n## ⚠️ DETECTED ANTI-PATTERNS")
            for i in ap[:5]:
                lines.append(f"- **{i.get('module', 'N/A')}**")
                for issue in i.get("issues", [])[:2]:
                    severity = issue.get("severity", "low")
                    lines.append(f"  - [{severity}] {issue.get('message', 'N/A')}")
