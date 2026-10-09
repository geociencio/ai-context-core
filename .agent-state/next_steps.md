# Next Steps - ai-context-core

**Last Updated:** 2026-10-08

## ✅ Completed in This Session

### Deep Cleanup & v4.0.0 Release
- ✅ **Anti-patterns surfaced**: fixed the bug where anti-pattern detections ran
  but were never reported; now rendered in `AI_CONTEXT.md`.
- ✅ **Dead code removed (breaking)**: retired the `CheckerRegistry` chain
  (`checker_registry`, `security_checker`, `tech_debt_checker`, `debt`), the
  `analyzer/pattern_base.py` facade, and unused symbols in `issues.py` /
  `registry.py`. Kept `optimization_checker.py` (live via `find_optimizations`).
- ✅ **Architecture purity**: moved `secrets_scanner.py` (file I/O) from
  `visitors/` to `providers/`.
- ✅ **Metric key contract**: `stats`/`analyze`/`ai_recommendations`/
  `context_metrics`/`summary_generator` now read metrics via `metric_keys`;
  complexity keys canonicalized in `formatter.py`.
- ✅ **Hygiene**: `ruff format .` applied (fixed the ~80-file drift); removed
  dead legacy wrappers in `singleton_rules.py` and the `observer_rules.py`
  re-export hop.
- ✅ **Release v4.0.0**: version bumped, `build`+`twine` added to dev group,
  tag `v4.0.0` pushed, GitHub release created with both artifacts.
  **PyPI upload still pending (manual)**.

## 🎯 Immediate Next Steps

- [x] **Start v4.1.0** — plan registered (`docs/maintenance/refactoring_plan_v4.1.0.md`).
- [ ] **WS-0** — unify config loading (canonical `providers.config_loader.load_config`).
- [ ] **WS-1..WS-5** — import graph, churn, anti-patterns, context-only mode, section toggles.
- [ ] **Publish to PyPI**: `uv run twine upload dist/*` (maintainer decision).
- [ ] Run `uv run python scripts/sync_metrics.py` to snapshot the new baseline.
- [ ] Apply `scripts/memory_prune.py --apply` to prune expired `next_steps`
  snapshots (>90 days).
- [ ] Register the `@architect` / `@qa_engineer` / `@auditor` subagents in your
  opencode client (declared in `opencode.json`).

## 📋 Future Enhancements

- [ ] Performance profiling on large projects (10k+ files).
- [ ] CI/CD release automation (PyPI upload from GitHub Actions).
- [ ] Custom rule engine (user-defined AST patterns).

## 🐛 Known Issues

**None blocking** — 302 tests passing locally and in Docker; `ai-ctx audit`
PASS (score 90.8); `validate_agent_system.py` PASS.

Note: the `ai-ctx Quality Score` is a heuristic, average-based metric. Removing
small high-maintainability shim files lowered it from 100 to ~90 without a real
quality regression; the release gate is 70.

## 🔧 Technical Debt

- Continue improving type hints across all modules.
- The `X.py` + `X_rules.py` split in `visitors/` is a deliberate
  complexity-management pattern (keeps modules under the CC 25 budget); do not
  consolidate without checking the self-score budget.

---

**Session Status:** ✅ Complete — deep cleanup + v4.0.0 release (PyPI pending).
