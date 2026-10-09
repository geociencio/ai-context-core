# Agentic Forge Adoption — Migration Report

**Date**: 2026-10-08
**Author**: @architect (+ @qa_engineer verification)
**Scope**: Migrate ai-context-core's agentic system onto the **agentic-forge** framework.

---

## 1. Context

ai-context-core sat at **Gen 8** (opencode-native, but with no `forge.toml` and no
submodule) with a duplicated, drifting agentic system. It was migrated onto the
**agentic-forge** framework (https://codeberg.org/geociencio/agentic-forge, MIT),
which separates the re-usable framework (git submodule at `.agent/`) from
project-owned state (`.agent-state/`).

### Target model

```
ai-context-core/
├── .agent/           ← git submodule → agentic-forge v1.2.0
├── .agent-state/     ← project-owned state + overlay skills
├── forge.toml        ← [forge].framework/.state + [project] thresholds
├── opencode.json     ← native subagents (allow/ask/deny) + skills.paths
└── AGENTS.md         ← canonical root override
```

---

## 2. What was done (F1–F5)

### F1 — State/path split
- Moved `memory/`, `history/`, `task.md`, `next_steps.md`, `task_improvements.md` →
  `.agent-state/` (`git mv`).
- Added `forge.toml`:
  ```toml
  [forge]
  framework = ".agent"
  state = ".agent-state"

  [project]
  name = "ai-context-core"
  test_dirs = ["tests"]
  analyzer_command = "uv run ai-ctx analyze --path ."
  max_cc = 25
  module_size_limit = 400
  ```

### F2 — Content split
- Moved 5 project-specific skills to the overlay `.agent-state/skills/`:
  `domain-logic`, `project-context`, `debug-specialist`, `skill-authoring`, `tech-stack`.
- Updated `project-context` structure notes (`.agent/` submodule + `.agent-state/`).

### F3 — Submodule
- `.agent/` became a git submodule of `agentic-forge`, pinned at `v1.2.0` (`2de22cf`).
- CI (`ci.yml`, `release.yml`): `submodules: recursive`.

### F4 — Tooling
- Removed `scripts/{validate_agent_system,memory_prune}.py`.
- Kept `scripts/sync_metrics.py` as the collector/adapter (repointed to
  `.agent-state/memory/agent_metrics.json`).
- Updated the local `.git/hooks/pre-commit` to call `python3 .agent/tools/forge.py validate`.

### F5 — Cleanup + docs
- Removed `agentic_framework_guide.md` and `agentic_framework_skeleton.zip`.
- `pyproject.toml`: ruff now excludes `.agent` and `.agent-state`.
- `opencode.json`: `skills.paths = [".agent/skills", ".agent-state/skills"]`.
- Rewrote root `AGENTS.md`; updated `.analyzerignore`.

---

## 3. Verification (gates)

| Gate | Result |
| :--- | :--- |
| `python .agent/tools/forge.py validate` | ✅ 14 skills (9 framework + 5 overlay), 14 workflows |
| `python .agent/tools/forge.py validate --conflicts` | ✅ no overlaps |
| `git submodule status` | ✅ `.agent` @ `v1.2.0` |
| `uv run ruff check .` | ✅ clean |
| `uv run pytest -q` | ✅ 299 passed |

---

## 4. References

- Framework repo: https://codeberg.org/geociencio/agentic-forge (MIT)
- Session log: `docs/sessions/session_2026-10-08_agentic_forge_adoption.md`
- Unified plan: `docs/plans/implementation_plan_unify_agentic_systems.md` (sec_interp repo)
