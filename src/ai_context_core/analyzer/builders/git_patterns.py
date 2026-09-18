"""Summarizers for git churn and design patterns."""

from .summarizer_base import BaseSummarizer


class GitPatternsSummarizer(BaseSummarizer):
    """Builds sections for git analysis and detected patterns."""

    def build_git(self) -> str:
        git = self.analyses.get("git", {})
        if not git:
            return ""
        res = []
        churn = git.get("churn", {})
        if churn.get("available"):
            res.append(f"### Code Churn (last {churn.get('period_days')} days)")
            res.append(
                f"- **Files Changed**: {churn.get('files_changed', 0)}\n- **Additions**: +{churn.get('added', 0)}\n- **Deletions**: -{churn.get('deleted', 0)}\n- **Total Churn**: {churn.get('total_churn', 0)}"
            )

        hot = git.get("hotspots", [])
        if hot:
            res.append("\n### 🔥 Hotspots")
            for h in hot[:5]:
                res.append(f"- `{h.get('path', 'N/A')}`: {h.get('commits', 0)} commits")
        return "\n".join(res)

    def build_patterns(self) -> str:
        pats = self.analyses.get("patterns", {})
        if not pats:
            return ""
        res = []
        for name, occs in pats.items():
            res.append(f"### {name}")
            for occ in occs[:5]:
                res.append(
                    f"- **{occ.get('class') or occ.get('name') or 'N/A'}** in `{occ.get('module', 'N/A')}` ({occ.get('confidence', 0)}%)"
                )
        return "\n".join(res)
