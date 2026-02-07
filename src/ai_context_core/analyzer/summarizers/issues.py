"""Summarizers for issues, debt, and recommendations."""

from .base import BaseSummarizer

class IssuesSummarizer(BaseSummarizer):
    """Builds sections for critical issues and optimizations."""

    def build_issues(self) -> str:
        lines = []
        sec = self.analyses.get("security", [])
        if sec:
            lines.append("### 🔒 Security Issues:")
            for i in sec[:3]:
                lines.append(
                    f"- **{i['module']}**: {i['total_issues']} issues (Max: {i['max_severity'].upper()})"
                )

        debt = self.analyses.get("debt", [])
        if debt:
            lines.append("\n### 🏗️ Critical Technical Debt:")
            for i in [d for d in debt if d.get("severity_score", 0) >= 4][:5]:
                lines.append(
                    f"- **{i['module']}**: {i['total_issues']} issues (Score: {i['severity_score']})"
                )

        circ = self.analyses.get("dependencies", {}).get("circular_dependencies", [])
        if circ:
            lines.append("\n### 🔄 Circular Dependencies:")
            for cycle in circ[:3]:
                lines.append(
                    f"- {' -> '.join(cycle) if isinstance(cycle, list) else str(cycle)}"
                )

        return "\n".join(lines)

    def build_recommendations(self) -> str:
        opts = self.analyses.get("optimizations", [])
        if not opts:
            return ""
        res = []
        for o in opts[:3]:
            res.append(f"### {o.get('module')}")
            for sug in o.get('suggestions', [])[:2]:
                res.append(f"- {sug.get('message', 'N/A')}")
        return "\n".join(res)
