"""Builders for git and technology sections."""

from .context_base import BaseContextBuilder
from typing import List


class GitTechBuilder(BaseContextBuilder):
    """Adds git analysis and technology summary."""

    def build(self, lines: List[str]) -> None:
        git_data = self.analyses.get("git", {})
        if git_data:
            lines.append("\n## 🔄 GIT AND EVOLUTION")
            hot = git_data.get("hotspots", [])
            if hot:
                lines.append("### Top Hotspots:")
                for h in hot[:5]:
                    lines.append(f"- `{h['path']}` ({h['commits']} commits)")

            ch = git_data.get("churn", {})
            if ch.get("available"):
                lines.append(f"### Recent Churn ({ch.get('period_days')} days):")
                lines.append(f"- Total lines changed: {ch.get('total_churn')}")

        s = self.analyses.get("structure", {})
        lines.append("\n## 🔑 PROJECT KEYWORDS")
        ft = list(s.get("file_types", {}).keys())
        lines.append(f"- **Technologies**: {', '.join(ft[:8])}")
