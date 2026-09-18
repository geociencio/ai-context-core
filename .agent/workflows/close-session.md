---
description: Procedure to end a work session, update logs, and archive results
agent: qa_engineer
skills: [qa-docker, commit-standards, agentic-memory, documentation-standards, changelog-generator]
validation: |
  - Verify that all logs are updated
  - Confirm that tests pass before closing
  - Validate that .agent/next_steps.md exists and has clear content
---

# Workflow: Close Session

Closes the development cycle, converting technical work into historical memory for the next session.

### 1. Memory Update (Logs & Roadmap)

🤖 **Agent Action**: Validate that all critical files are updated.

- **Session Topic**: Define a short name (e.g. `metrics_contract`).
- **Task Persistence**: Ensure `.agent/task.md` reflects actual progress; archive completed phases in `.agent/history/tasks/`.
- **`.agent/next_steps.md`**: **[CRITICAL]** Create/update with the "handover": what's missing, pending errors, resume command.
- **Next Steps Archiving**: Copy `next_steps.md` to `.agent/history/next_steps/next_steps_YYYY-MM-DD.md`.
- **`docs/maintenance/session_YYYY-MM-DD_[TOPIC].md`**: **[MANDATORY]** Create with the session's technical summary.
- **`docs/DEVELOPMENT_LOG.md`**: **[CRITICAL]** Add entry following the `documentation-standards` format.
- **`CHANGELOG.md`**: Record user-visible changes in `[Unreleased]` using the `changelog-generator` skill (interpretive: use `git log` to read session commits and write directly to CHANGELOG.md — do not run Python scripts).

### 2. Final Verification (Safety Net)

🤖 **Agent Action**: Use `qa-docker` to validate stability before closing.

```bash
uv run ruff check . && uv run ruff format --check .
make docker-test
```

🤖 **Agent Action**: Verify tests pass; alert if there are failures.

### 3. Final Memory Synchronization (AI)

🤖 **Agent Action (System Validation)**:
```bash
uv run python scripts/validate_agent_system.py
```

🤖 **Agent Action (Learning)**: Identify the 3 most important technical lessons this session and update YAML entries in `AGENT_LESSONS.md` + `agent_metrics.json`.

🤖 **Agent Action**: Update AI_CONTEXT.md and validate `next_steps.md`:
```bash
uv run ai-ctx analyze --path . && cat .agent/next_steps.md
```

### 4. Local Commit

🤖 **Agent Action**: Use `commit-standards` to generate an appropriate message.

```bash
git add .
git commit -m "chore(docs): close session [TOPIC]"
```

*If the pre-commit hook persists in failing:* review the errors, `git add` again if there were automatic changes, and repeat the commit.

### 5. Summary for the User

Generate a final message listing: updated log files, test status, content of `next_steps.md`, and the suggestion to resume with `/start-session`.

## Expected Result
- Session memory persisted in logs and `next_steps.md`.
- Repository clean and technically validated.
- Clear instructions to resume without context loss.

**Philosophy**: A session doesn't end when the code works, but when the story is told.
