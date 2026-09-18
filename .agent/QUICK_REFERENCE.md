# Quick Reference: Workflows + Skills System

**Created**: 2026-09-17 (Generation 8)
**Version**: 3.0

---

## Executive Summary

The ai-context-core project features a system of **14 skills** and **11 workflows** integrated to automate AI-assisted development. The system runs **natively under opencode** (Generation 8): the root `AGENTS.md` is the single source of truth, subagents are registered in `opencode.json`, and skills are discovered via `skills.paths`.

---

## Available Skills (14)

| Skill | Description | When to Use |
|:------|:------------|:------------|
| [agentic-memory](file://.agent/skills/agentic-memory/SKILL.md) | Lessons and patterns management | Extracting meta-lessons, preferences |
| [changelog-generator](file://.agent/skills/changelog-generator/SKILL.md) | Automated changelog from git commits | Writing release notes, CHANGELOG updates |
| [coding-standards](file://.agent/skills/coding-standards/SKILL.md) | Project coding standards | Writing Python code, refactoring |
| [commit-standards](file://.agent/skills/commit-standards/SKILL.md) | Conventional Commits standards | Creating commits, validating messages |
| [debug-specialist](file://.agent/skills/debug-specialist/SKILL.md) | Systematic bug resolution | Reproducing and fixing bugs |
| [documentation-standards](file://.agent/skills/documentation-standards/SKILL.md) | Logs and project history standards | Updating development/maintenance logs |
| [domain-logic](file://.agent/skills/domain-logic/SKILL.md) | Analysis rules, validation, core processing | New rules, metric calculation |
| [i18n-standards](file://.agent/skills/i18n-standards/SKILL.md) | i18n standards for the analyzer | Modifying the i18n visitor |
| [project-context](file://.agent/skills/project-context/SKILL.md) | Project purpose and architecture | Starting tasks, overviews |
| [qa-docker](file://.agent/skills/qa-docker/SKILL.md) | Docker testing environments | Running integration tests |
| [release-management](file://.agent/skills/release-management/SKILL.md) | Python package release process | Preparing releases, versioning |
| [skill-authoring](file://.agent/skills/skill-authoring/SKILL.md) | Designing new agent skills | Creating new skills |
| [tech-stack](file://.agent/skills/tech-stack/SKILL.md) | Toolchain, uv, quality tools | Installing dependencies |
| [testing-standards](file://.agent/skills/testing-standards/SKILL.md) | Automated testing with pytest/Docker | Writing tests, strategies |

---

## Available Workflows (11)

### Daily Development

| Workflow | Agent | Purpose |
|:---------|:------|:---------|
| [/start-session](file://.agent/workflows/start-session.md) | architect | Start session with synced context |
| [/create-commit](file://.agent/workflows/create-commit.md) | qa_engineer | Commit with quality validation |
| [/run-tests](file://.agent/workflows/run-tests.md) | qa_engineer | Run tests with interpretation |
| [/close-session](file://.agent/workflows/close-session.md) | qa_engineer | Close session with memory update |

### Refactoring and Quality

| Workflow | Agent | Purpose |
|:---------|:------|:---------|
| [/refactor-code](file://.agent/workflows/refactor-code.md) | architect | Refactor code with validation |
| [/audit-plugin](file://.agent/workflows/audit-plugin.md) | auditor | Full self-analysis with ai-ctx |
| [/fix-linting](file://.agent/workflows/fix-linting.md) | qa_engineer | Automatically fix style issues |

### Features and Review

| Workflow | Agent | Purpose |
|:---------|:------|:---------|
| [/build-feature](file://.agent/workflows/build-feature.md) | architect | Pipeline for new features |
| [/ia-critic](file://.agent/workflows/ia-critic.md) | auditor | Plan review and validation |

### Release and Standards

| Workflow | Agent | Purpose |
|:---------|:------|:---------|
| [/release-package](file://.agent/workflows/release-package.md) | qa_engineer | Release to PyPI |
| [/verify-standards](file://.agent/workflows/verify-standards.md) | architect | Audit agent system integrity |

---

## Quality Gate Scripts

| Script | Command |
|--------|---------|
| Full analysis | `uv run ai-ctx analyze --path .` |
| Metric sync | `uv run python scripts/sync_metrics.py` |
| Agent system validation | `uv run python scripts/validate_agent_system.py` |
| Memory prune | `uv run python scripts/memory_prune.py` |
| Lint check | `uv run ruff check .` |
| Lint fix | `uv run ruff check --fix . && uv run ruff format .` |
| Test suite | `uv run pytest -q` |
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

## Runtime

This system runs natively on **opencode**. Subagents are registered in `opencode.json`; skills are discovered via `skills.paths`. The root `AGENTS.md` is the single source of truth — see `workflows/index.md` for per-workflow command details.
