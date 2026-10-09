# Session 2026-10-08 — Agentic Forge Adoption (F1–F5)

**Topic**: `agentic_forge_adoption`
**Agent role**: @architect (+ @qa_engineer for verification)
**Result**: ✅ COMPLETE — ai-context-core now consumes `agentic-forge` `v1.2.0` as a submodule.

---

## Objective

Migrate ai-context-core's Gen 8 agentic system onto the **agentic-forge** framework
(Codeberg, MIT), separating the re-usable framework (submodule at `.agent/`) from
project-owned state (`.agent-state/`). Second of three sibling projects to adopt the
unified pattern (after `qgis-plugin-analyzer`).

---

## What was done

### F1 — State/path split
- Moved `memory/`, `history/`, `task.md`, `next_steps.md`, `task_improvements.md` →
  `.agent-state/` (`git mv`).
- Added `forge.toml` (`framework = ".agent"`, `state = ".agent-state"`,
  `max_cc = 25`, `module_size_limit = 400`).

### F2 — Content split
- Moved the 5 project-specific skills to the overlay `.agent-state/skills/`:
  `domain-logic`, `project-context`, `debug-specialist`, `skill-authoring`, `tech-stack`.
- Updated `project-context` structure notes (`.agent/` submodule + `.agent-state/`).

### F3 — Submodule
- `.agent/` converted to a git submodule of `agentic-forge`, pinned at `v1.2.0`
  (`2de22cf`).
- CI (`ci.yml`, `release.yml`): `submodules: recursive` on all checkout steps.

### F4 — Tooling
- Removed `scripts/{validate_agent_system,memory_prune}.py`.
- Kept `scripts/sync_metrics.py` as the collector/adapter (repointed to
  `.agent-state/memory/agent_metrics.json`).

### F5 — Cleanup + docs
- Removed `agentic_framework_guide.md` and `agentic_framework_skeleton.zip`.
- `pyproject.toml`: ruff now excludes `.agent` and `.agent-state`.
- `opencode.json`: `skills.paths = [".agent/skills", ".agent-state/skills"]`.
- Rewrote root `AGENTS.md` (framework skills + overlay + `forge.py` tooling).
- Updated `.analyzerignore` (`.agent/`, `.agent-state/`, `forge.toml`, `.gitmodules`).

---

## Verification

- `python .agent/tools/forge.py validate` → 14 skills (9 framework + 5 overlay),
  14 workflows, no broken refs.
- `git submodule status` → `.agent` @ `v1.2.0`.
- `uv run ruff check .` → clean.
- `uv run pytest` → (see DEVELOPMENT_LOG test count).

---

## Resume

ai-context-core migration complete. Remaining: `qgis-plugin-manager` (Part D), then a
cross-repo gate confirming all three pin the same framework version.
