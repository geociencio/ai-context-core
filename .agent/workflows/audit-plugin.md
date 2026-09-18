---
description: Run ai-ctx on its own codebase for quality self-audit
agent: auditor
skills: [project-context, testing-standards]
validation: |
  - Verify analysis completes without errors
  - Confirm no critical/blocking issues
  - Review PROJECT_SUMMARY.md
---

# Workflow: Audit Plugin (Self-Analysis)

Runs `ai-context-core` on its own source code to detect quality regressions, security issues, and standards violations.

### 1. Run Full Analysis
```bash
uv run ai-ctx analyze .
```

### 2. Review Results

🤖 **Agent Action**: Read and interpret the analysis output.

- Check `PROJECT_SUMMARY.md` for overall scores.
- Review any `HIGH` or `CRITICAL` severity issues.
- Compare scores against the previous baseline in `.agent/memory/agent_metrics.json`.

### 3. Triage Issues

| Severity | Action |
|----------|--------|
| CRITICAL | Fix immediately, block release |
| HIGH | Log in `task.md`, fix this session |
| MEDIUM | Log in `next_steps.md` for next phase |
| LOW | Accept or log as technical debt |

### 4. Update Metrics
After triage, run `uv run python scripts/sync_metrics.py` to update `.agent/memory/agent_metrics.json`.

### Expected Results
- All tests passing.
- No new CRITICAL or HIGH issues.
- Maintainability ≥ 75/100.
