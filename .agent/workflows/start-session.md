---
description: Standard and robust procedure for starting a "Local First" development session
agent: architect
skills: [project-context, qa-docker, agentic-memory]
validation: |
  - Verify that all tests pass
  - Confirm that AI_CONTEXT.md is updated with recent metrics
  - Validate that there are no regressions in cyclomatic complexity
---

# Workflow: Start Session

Optimizes the start of development by ensuring a synchronized, contextualized, and validated environment.

### 1. Context Tuning (CRITICAL)
// turbo
```bash
uv run ai-ctx analyze . && cat .agent/next_steps.md && cat .agent/memory/AGENT_LESSONS.md
```

🤖 **Agent Action**: Validate active tasks.

- **Task management**:
    - Verify if `.agent/task.md` exists.
    - If it exists: show the content ("Current Status").
    - If it does NOT exist: create it based on `next_steps.md`.

Review the following files in this order:
- `.agent/next_steps.md`: **The Witness (Source of Truth)** — exact starting point and immediate goals.
- `.agent/task.md`: **Active Board** — must align with `next_steps.md`.
- `.agent/memory/AGENT_LESSONS.md`: **The Brain** — error patterns and preferences.
- `AI_CONTEXT.md`: Architectural context and long-term metrics.
- `docs/DEVELOPMENT_LOG.md`: Summary of the last session (reverse chronological).

### 2. Quick Quality Scan
```bash
uv run ai-ctx stats
```

### 3. Integrity Validation (Tests)
```bash
uv sync
```
🤖 **Agent Action**: Verify there are no dependency conflicts.

### 4. Status Verification (Sanity Check)
All tests must pass.

*Option A (Docker - Recommended):*
```bash
make docker-test
```

*Option B (Local):*
```bash
uv run pytest -q
```

## Expected Result
- Synchronized and validated environment (all tests OK).
- Clear mental map of pending tasks in `next_steps.md`.
- Agent operating with the correct roles and skills loaded.

## Structured Session Status
🤖 **Agent Action**: Conclude the initialization with:
```yaml
session_init: success
context_sync: complete
active_task: [task_name]
current_metrics:
  tests: [count]
  quality_score: [score]
```

**Philosophy**: Start coding knowing exactly what happened yesterday and with specialized context loaded.
