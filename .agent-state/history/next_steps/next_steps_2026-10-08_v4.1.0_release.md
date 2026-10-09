# Next Steps - ai-context-core

**Last Updated:** 2026-10-08

## ✅ Completed in This Session

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
  release created. **PyPI upload deferred (manual)**.

## 🎯 Immediate Next Steps

- [ ] **Publish v4.1.0 to PyPI**: `uv run twine upload dist/*` (maintainer decision).
- [ ] Register the `@architect` / `@qa_engineer` / `@auditor` subagents in your
  opencode client (declared in `opencode.json`).
- [ ] Apply `scripts/memory_prune.py --apply` to prune expired `next_steps`
  snapshots (>90 days).

## 📋 Future Enhancements

- [ ] Performance profiling on large projects (10k+ files).
- [ ] CI/CD release automation (PyPI upload from GitHub Actions).
- [ ] Custom rule engine (user-defined AST patterns).

## 🐛 Known Issues

**None blocking** — 315 tests passing; `ai-ctx audit` PASS (score 90.1).

Note: the `ai-ctx Quality Score` is a heuristic, average-based metric. Removing
small high-maintainability shim files lowered it from 100 to ~90 without a real
quality regression; the release gate is 70. Also, config changes do not
invalidate the module cache, so `ai-ctx analyze` without `--no-cache` can show
stale antipattern/i18n results (pre-existing).

## 🔧 Technical Debt

- Continue improving type hints across all modules.
- The `X.py` + `X_rules.py` split in `visitors/` is a deliberate
  complexity-management pattern (keeps modules under the CC 25 budget); do not
  consolidate without checking the self-score budget.
- The generated artifacts (`AI_CONTEXT.md`, `PROJECT_SUMMARY.md`,
  `project_context.json`) have non-deterministic sections (patterns, unused
  imports); consider a deterministic ordering pass.

---

**Session Status:** ✅ Complete — v4.1.0 released (GitHub), PyPI pending.
