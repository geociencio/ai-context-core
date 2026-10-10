# Proposal: make `release-package` config-driven (agentic-forge)

**Status**: PROPOSED — owned by `agentic-forge` (framework submodule)
**Date**: 2026-10-10
**Origin**: ai-context-core v5.1.0 release prep (plan
`docs/plans/implementation_plan_v5.1_alignment_hardening.md`, WS-2 / P4)
**Target**: `.agent/workflows/release-package.md` +
`.agent/skills/release-management/SKILL.md`

## Problem

The generic `/release-package` workflow hardcodes assumptions that do not hold for
every consumer:

1. Step 2 bumps only `pyproject.toml` — consumers may keep the version in several
   places (e.g. `__init__.py` fallback, `uv.lock`).
2. Step 3 runs `mypy .` unconditionally — some projects use `ruff` only and must
   not run `mypy`.
3. It calls `twine upload dist/*`, but some maintainers publish to PyPI **manually**.
4. Step 4 `git add pyproject.toml CHANGELOG.md README.md docs/` omits `src/`,
   `tests/`, `AGENTS.md`, `forge.toml`, `.agent-state/` and fixtures.
5. No hook to refresh project metrics/agentic ground truth (e.g. a `sync_metrics.py`).
6. No awareness that the test suite may regenerate tracked artifacts (needing a
   separate `chore(docs)` commit).

Today these are all patched per-project (see ai-context-core's
`.agent-state/skills/release-ai-context-core/SKILL.md`), which duplicates guidance.

## Proposed change

Make the workflow **config-driven** via `forge.toml [project]`:

```toml
[project]
# ...
version_files = ["pyproject.toml", "src/<pkg>/__init__.py", "uv.lock"]
typecheck_command = ""                     # empty -> skip (no hardcoded mypy)
metrics_command = "uv run python scripts/sync_metrics.py"
pypi_manual = true                         # agent stops before twine upload
regenerated_artifacts = ["AI_CONTEXT.md", "PROJECT_SUMMARY.md"]
```

Workflow deltas:

- **Step 2**: iterate `version_files` (best-effort per file type) instead of a
  single hardcoded `pyproject.toml`.
- **Step 3**: run `typecheck_command` only when set; keep `pytest` + `ruff`.
- **Step 4**: build the `git add` set from `src/`, `tests/`, the version files,
  `AGENTS.md`, `forge.toml`, the state dir and `docs/` — or use a documented
  explicit list.
- **New step**: run `metrics_command` when set.
- **New step**: commit `regenerated_artifacts` as a separate `chore(docs)` commit.
- **Step 5**: when `pypi_manual = true`, stop at build + `twine check` +
  `gh release create` and print the `twine upload` hand-off.

## Migration

- Additive: missing keys fall back to the current behavior, so existing consumers
  are unaffected.
- `typecheck_command` default empty changes behavior for projects that relied on
  the implicit `mypy` — document in the framework CHANGELOG.

## Rationale / references

- ai-context-core ADR-0008 (context-only) and its release overlay skill.
- Lesson: PyPI uploads are manual; `mypy` must be avoided (ruff-only); pytest
  dirties generated artifacts.
