"""Summarizer for git evolution (churn and hotspots)."""

from .summarizer_base import BaseSummarizer


class GitSummarizer(BaseSummarizer):
    """Builds the git evolution section (churn and hotspots)."""

    def build_git(self) -> str:
        """Render the git churn/hotspots section."""
        git = self.analyses.get("git", {})
        if not git:
            return ""
        res = []
        churn = git.get("churn", {})
        if churn.get("available"):
            res.append(f"### Code Churn (last {churn.get('period_days')} days)")
            res.append(
                f"- **Files Changed**: {churn.get('files_changed', 0)}\n"
                f"- **Additions**: +{churn.get('added', 0)}\n"
                f"- **Deletions**: -{churn.get('deleted', 0)}\n"
                f"- **Total Churn**: {churn.get('total_churn', 0)}"
            )

        hot = git.get("hotspots", [])
        if hot:
            res.append("\n### 🔥 Hotspots")
            for h in hot[:5]:
                res.append(f"- `{h.get('path', 'N/A')}`: {h.get('commits', 0)} commits")
        return "\n".join(res)


# Backward-compatible alias (the design-pattern half was removed in v5.0.0).
GitPatternsSummarizer = GitSummarizer
