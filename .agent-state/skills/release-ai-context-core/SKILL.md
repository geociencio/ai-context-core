---
name: release-ai-context-core
description: Project-specific overlays for releasing ai-context-core on top of the framework /release-package workflow.
trigger: when preparing a release, bumping the version, or running /release-package.
---

# Release — ai-context-core Overlay

Project-owned deltas layered on the framework `/release-package` workflow and the
`release-management` skill. The framework covers the generic path; apply these
specifics on top.

## When to use this skill
- When bumping `ai-context-core`'s version.
- When running `/release-package`.
- When writing the CHANGELOG / release notes / development log for a release.

## Non-negotiables

1. **Version in three places** (must match the tag):
   - `pyproject.toml` → `version`
   - `src/ai_context_core/__init__.py` → `__version__` fallback string
   - `uv.lock` → the `ai-context-core` package `version`
2. **Skip `mypy`.** `ruff` is the single linter/formatter. Run
   `uv run ruff check . && uv run ruff format --check .`.
3. **PyPI is automated.** `.github/workflows/release.yml` uses PyPI **Trusted
   Publishing** (OIDC): a tag creates a draft GitHub Release, and publishing that
   draft runs the version guard, lint, tests, build, `twine check`, PyPI publish
   and attaches the distributions. The human approval gate is publishing the
   draft, not running `twine upload`.
4. **Sync the agentic ground truth.** Run `uv run python scripts/sync_metrics.py`
   so `.agent-state/memory/agent_metrics.json` matches reality (tests + quality).
5. **Separate `chore(docs)` commit.** `pytest` regenerates the root artifacts
   (`AI_CONTEXT.md`, `PROJECT_SUMMARY.md`, `project_context.json`,
   `context_manifest.json`); commit them separately from the release bump.
6. **Complete `git add` set.** `src/`, `tests/`, `AGENTS.md`, `forge.toml`,
   `.agent-state/`, `docs/`, `scripts/` (the framework workflow list is
   incomplete).

## Prerequisites (one-time, maintainer)

- PyPI → project `ai-context-core` → **Publishing** → add a GitHub trusted
  publisher: owner `geociencio`, repository `ai-context-core`, workflow
  `release.yml`, environment `pypi`.
- GitHub → **Settings → Environments** → create `pypi` (optionally require
  reviewers). The workflow references this environment.
- `PYPI_TOKEN` is not needed; remove it after a successful OIDC publish.

## Order of operations

1. Confirm green: `uv run ruff check . && uv run pytest -q`.
2. Bump the three version sites; verify `uv run ai-ctx --version`.
3. Validate the guard: `uv run python scripts/check_release_version.py --tag vX.Y.Z`.
4. Update `CHANGELOG.md` (move `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`) and
   create `docs/releases/notes/vX.Y.Z.md`; add a `docs/DEVELOPMENT_LOG.md` entry.
5. `uv run python scripts/sync_metrics.py`; regenerate artifacts.
6. Commit: `chore(release): prepare vX.Y.Z`; commit artifacts as `chore(docs): ...`.
7. Optional local safety net: `rm -rf dist && uv build && uv run twine check dist/*`.
8. `git tag -a vX.Y.Z -m "Release vX.Y.Z"` and push the tag. The workflow creates
   the draft.
9. Publish the draft on GitHub (`gh release edit vX.Y.Z --draft=false ...`). This
   triggers tests, build, PyPI publish and asset attachment.
10. Verify `gh run view <run-id>` (all jobs success) and the PyPI JSON for X.Y.Z.

## Quality Checklist
- [ ] Are all three version sites updated and consistent?
- [ ] Does `scripts/check_release_version.py` pass for the tag?
- [ ] Did `ruff check` + `pytest` pass?
- [ ] Is `agent_metrics.json` synced?
- [ ] Is there a `chore(docs)` commit for regenerated artifacts?
- [ ] Is the GitHub release published and did `publish-pypi` succeed?
- [ ] Are the wheel/sdist attached to the GitHub release and visible on PyPI?
