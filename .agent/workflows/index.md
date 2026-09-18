# Workflow Quick Reference

> Maps each `.agent/workflows/*.md` to concrete opencode actions.
> For humans: "I want to run X, what do I tell the agent?"
> For agents: "User said /X, what do I actually do?"

---

## Daily Development

### `/start-session`
**What happens**:
```
uv run ai-ctx analyze --path .
cat .agent/next_steps.md
cat .agent/task.md
cat .agent/memory/AGENT_LESSONS.md
uv sync
uv run pytest -q
```

### `/close-session`
**What happens**:
```
uv run pytest -q
uv run python scripts/validate_agent_system.py
# Update AGENT_LESSONS.md with lessons
# Update next_steps.md; archive to history/
# Create docs/maintenance/session_YYYY-MM-DD_[topic].md
# Update docs/DEVELOPMENT_LOG.md and CHANGELOG.md
git add . && git commit -m "chore(docs): close session [topic]"
```

### `/create-commit`
**What happens**:
```
uv run ruff check --fix .
uv run ruff format .
git add [files] && git commit -m "[msg]"
```

### `/run-tests`
**What happens**: `uv run pytest tests/ -v --cov=src/ai_context_core`

---

## Refactoring & Quality

### `/refactor-code`
**What happens**: Reads coding-standards → applies changes → validates tests → ruff check.

### `/audit-plugin`
**What happens**: `uv run ai-ctx analyze --path .` → review `PROJECT_SUMMARY.md`.

### `/fix-linting`
**What happens**: `uv run ruff check --fix . && uv run ruff format .`

---

## Features & Review

### `/build-feature`
**What happens**: Reads domain-logic → implements → `/ia-critic` review → `/create-commit`.

### `/ia-critic`
**What happens**: Reads AGENT_LESSONS.md → cross-references AGENTS.md → issues verdict.

---

## Release & Standards

### `/release-package`
**What happens**: Reads release-management → audit → build → `twine check`.

### `/verify-standards`
**What happens**: `uv run python scripts/validate_agent_system.py --graph`.

---

## Quality Gate Commands (Direct)

| Gate | Command |
|------|---------|
| Full analysis | `uv run ai-ctx analyze --path .` |
| Lint check | `uv run ruff check .` |
| Test suite | `uv run pytest -q` |
| Agent validation | `uv run python scripts/validate_agent_system.py` |
| Memory prune | `uv run python scripts/memory_prune.py` |
| Metric sync | `uv run python scripts/sync_metrics.py` |
| Build check | `uv run python -m build && twine check dist/*` |

---

## Quick Reference Card

```
Start session:            /start-session
Close session:            /close-session [topic]
Quality commit:           /create-commit [message]
Run tests:                /run-tests

Safe refactor:            /refactor-code [file]
Self-audit:               /audit-plugin
Auto-linting:             /fix-linting

New feature:              /build-feature [desc]
Plan review:              /ia-critic

Release:                  /release-package
Verify standards:         /verify-standards
```
