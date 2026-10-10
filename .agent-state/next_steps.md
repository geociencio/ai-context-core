# Next Steps - ai-context-core

**Last Updated:** 2026-10-10

## ✅ Released — v5.0.1 Post-Release Cleanup

- **Status**: ✅ **Released 2026-10-10** — tag `v5.0.1`, GitHub release + **PyPI**
  (`ai-context-core==5.0.1` confirmed live).
- Single render path (`compile_context → render_context` for all sources);
  retired v4 residue (`ContextAggregator`/`deprecations.py`, `graph_engine`, ...);
  repo hygiene; `ast.Constant` fix; pyproject metadata.
- See `docs/reviews/audit_architecture_redundancies_v500.md` (audit P0–P4) and
  `docs/releases/notes/v5.0.1.md`.
- **Deferred**: package renames (`analyzer/providers → engine`, split
  `parser`/`report`), R5 (unrendered payload), CLI coverage.

## ✅ Released — v5.0.0 Context-Only Contract

- **Status**: ✅ **Released 2026-10-09** — tag `v5.0.0`, GitHub release + **PyPI** (`ai-context-core==5.0.0` confirmed live).
- Plan: `docs/plans/implementation_plan_ai_context_core_context_only_v5.md`
- Review: `docs/reviews/ia_critic_implementation_plan_context_only_v5.md`
- ADR: `docs/adr/0008-context-only-contract.md`
- **F0 done**: ADR-0008 accepted; `REMOVAL_VERSION=5.0.0`; score→context-health
  naming recorded (CHANGELOG `[Unreleased]`, README notice). Feature freeze active.
- **F1 done**: `model/AnalysisResult` + `sources/` (builtin engine source, external
  qgis-analyzer adapter, hybrid pipeline) and `--source` on `analyze`/`context`;
  `engine.collect()` split for side-effect-free extraction.
- **F2 done**: context-only CLI surface (`ai-ctx --help`); removed `audit`, `inspect`,
  `qgis`, `security`, `patterns`, `full-scan`, `fix`, `scaffold`, `doctor`, `interactive`,
  `serve` (~50 analysis modules + qgis profile); hidden redirect stubs (one cycle);
  generator/aggregator re-scoped; `visitors/issues.py` split; golden regenerated.
  **Measured tests: 349 → 165.**
- **F3 done**: `context/budget.py` + `context/manifest.py`; `ai-ctx context
  --max-tokens N` (deterministic, strict cap) and `[context.budget]` per-section
  limits; `context_manifest.json` with exact per-section deltas
  (`total == header + sum(sections)`) + `_meta` provenance. Tests 165 → **177**.
- **F4 done**: `verify` (content-hash staleness, exit 1 on drift),
  `symbols [--grep]` (`symbols.json` with `file:line`), `health`
  (freshness/tokens/provenance), `context --check` CI gate. Tests 177 → **189**.
- **F5 deferred**: ecosystem alignment is owned by the sibling repos, not
  `ai-context-core` — `agentic-forge` (`project-context` skill),
  `qgis-plugin-analyzer` (README/cross-link), `sec_interp`
  (workflows `ai-ctx qgis`/`audit` → `qgis-analyzer` + `ai-ctx context`).
- **ai-context-core v5.0.0 scope is complete** (F0–F4 + divergence/optimization
  P0–P4). 182 tests passing; ruff clean.
- **Released**: version `5.0.0` synced (pyproject/`__init__`/uv.lock), build +
  `twine check` OK, tag + GitHub release, and **published to PyPI** by the
  maintainer (verified: PyPI reports `5.0.0` as latest).

## ✅ Completed in This Session

### v4.1.1 — Report Correctness Fixes (F1–F5)
- ✅ **F1 cache versioning**: `providers/fs_cache.py` now persists a `_meta`
  block (`schema`, analyzer `version`, config fingerprint) and discards
  mismatched caches; `engine.py` passes the config fingerprint. Stale results
  after tool upgrades/config edits can no longer be replayed.
- ✅ **F2 real security severity**: new `builders/security_severity.max_severity`
  ranks findings; `aggregator._aggregate_security` recomputes it on the AST-only
  and merge paths; `issues.py` adds a `… (+N more)` top-3 indicator.
- ✅ **F3 re-exports**: `visitors/import_export.collect_exported_names` +
  `ImportVisitor` treat `__all__` names as used; `builders/unused_imports`
  exempts package `__init__.py` via `[patterns.unused_imports].ignore_package_reexports`.
- ✅ **F4 code-scoped churn**: new `providers/git_churn.filter_churn` +
  `GitAnalyzer(exclusion_patterns=...)`; churn excludes non-analyzed paths and
  keeps `raw_*` git-wide totals; scoped from `engine` → `git_analysis`.
- ✅ **F5 conditional Processing note**: `builders/qgis_processing.has_processing_imports`
  drives `declares_processing`; `qgis_summarizer` only nags when processing is
  intended but no algorithm is found.
- ✅ **Tests**: 315 → **333** (+18). ruff clean; `ai-ctx audit` PASS (90.2).
- ✅ **Release v4.1.1**: version bumped (`4.1.0` → `4.1.1`), CHANGELOG `[4.1.1]`,
  release notes, DEVELOPMENT_LOG, golden fixtures refreshed, build + `twine check`,
  tag `v4.1.1` pushed, GitHub release created. **PyPI upload pending (credentials)**.
- ✅ **CHANGELOG repair**: added the missing `[4.1.0]` section and removed the
  stray `# DEVELOPMENT LOG` heading (moved the orphan entry to `DEVELOPMENT_LOG.md`).

### v4.1.0 — Context Map & Debt Prioritization (WS-0..WS-5)
- ✅ **WS-0 config**: unified config loading into `providers.config_loader.load_config`
  (TOML preferred, YAML legacy fallback); `config.loader.ConfigLoader` is now a
  `DeprecationWarning` facade.
- ✅ **WS-1 import graph**: resolved distribution-prefix and relative imports;
  rewrote the Mermaid diagram (collision-free IDs, class for all cited nodes).
  Self-analysis edges 28 → 45.
- ✅ **WS-2 churn**: `git log --numstat --find-renames` + per-file grouping; top-5
  churned files rendered.
- ✅ **WS-3 anti-patterns**: severity ordering, magic-number `allowlist`, and
  `min_severity` cutoff via `[patterns.antipatterns]`.
- ✅ **WS-4 context-only**: new `ai-ctx context` command; `analyze` score labeled
  heuristic; `audit` remains the sole gate.
- ✅ **WS-5 sections**: `[context].sections` toggles `AI_CONTEXT.md` sections;
  dropped `PROJECT KEYWORDS`; `__future__` excluded from unused imports.
- ✅ **Metrics adapter**: `sync_metrics.py` emits the framework-compatible
  `summary`/`last_session` schema.
- ✅ **Release v4.1.0**: version bumped (3 locations + CLI), CHANGELOG, release
  notes, DEVELOPMENT_LOG, build + `twine check`, tag `v4.1.0` pushed, GitHub
  release created, **published to PyPI**.

## 🎯 Immediate Next Steps

- [ ] **Manual (maintainer)**: publish v4.1.1 to PyPI — `uv run twine upload dist/*`.

_No agent-side blockers. PyPI uploads are always performed manually by the
maintainer (see `AGENT_LESSONS.md` → User Preferences); the agent stops at
build + `twine check` + GitHub release. Proceed with Future Enhancements below._

## 📋 Future Enhancements

- [ ] Performance profiling on large projects (10k+ files).
- [ ] CI/CD release automation (PyPI upload from GitHub Actions).
- [ ] Custom rule engine (user-defined AST patterns).

## 🐛 Known Issues

**None blocking** — 333 tests passing; `ai-ctx audit` PASS (score 90.2).

- **Metrics validator false positives**: `forge.py metrics validate` flags 5
  entries in the `.agent/` framework submodule — `scaffold/qgis/workflows/release-plugin.md`
  (CC≤10, 763 tests → SecInterp's domain values) and `skills/coding-standards/SKILL.md`
  ("complexity below 10" → generic guideline). These are template/domain values,
  not stale ai-context-core metrics (CC≤25, 333 tests). The validator scans
  `scaffold/` against this project's ground truth; treat as non-blocking until the
  framework excludes domain packs from ground-truth checks.

Note: the `ai-ctx Quality Score` is a heuristic, average-based metric. Removing
small high-maintainability shim files lowered it from 100 to ~90 without a real
quality regression; the release gate is 70. (Config changes now invalidate the
module cache via the F1 cache-fingerprint fix.)

## 🔧 Technical Debt

- Continue improving type hints across all modules.
- The `X.py` + `X_rules.py` split in `visitors/` is a deliberate
  complexity-management pattern (keeps modules under the CC 25 budget); do not
  consolidate without checking the self-score budget.
- The generated artifacts (`AI_CONTEXT.md`, `PROJECT_SUMMARY.md`,
  `project_context.json`) have non-deterministic sections (patterns, unused
  imports); consider a deterministic ordering pass.

---

**Session Status:** v5.0.0 F0 complete (contract + freeze); F1 (source layer) next.
(Also pending, manual: publish v4.1.1 to PyPI by the maintainer.)
