"""Builders for git and technology sections."""

from .context_base import BaseContextBuilder
from typing import List


class GitTechBuilder(BaseContextBuilder):
    """Adds git analysis (hotspots and churn)."""

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
                lines.append(f"- Total lines changed: {ch.get('total_churn')} (analyzed code)")
                raw_total = ch.get("raw_total_churn")
                if raw_total is not None and raw_total != ch.get("total_churn"):
                    lines.append(f"- Total lines changed (all tracked): {raw_total}")
                hot_paths = {h["path"] for h in hot}
                per_file = ch.get("per_file", {})
                top_churn = sorted(
                    per_file.items(),
                    key=lambda kv: kv[1]["added"] + kv[1]["deleted"],
                    reverse=True,
                )[:5]
                if top_churn:
                    lines.append("- Top churned files:")
                    for path, counts in top_churn:
                        total = counts["added"] + counts["deleted"]
                        marker = " 🔥" if path in hot_paths else ""
                        lines.append(
                            f"  - `{path}` (+{counts['added']} -{counts['deleted']}, {total}){marker}"
                        )
