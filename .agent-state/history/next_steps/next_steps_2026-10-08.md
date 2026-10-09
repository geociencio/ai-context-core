# Next Steps - ai-context-core

**Last Updated:** 2026-10-08

## ✅ Completed in This Session

### Redundancy Cleanup (`redundancy_optimization_plan.md`)
- ✅ **Phase A — Dead code**: Removed `visitors/legacy.py`,
  `visitors/antipattern_orchestrator.py`, `builders/scorer.py`,
  `builders/graph_engine.py`, `engine_config.py`, the broken
  `check_complexity.py`, plus duplicate `HalsteadVisitor`, `_mask_secret`,
  `analyze_structure`, `count_file_types`/`calculate_size_stats` and the
  `scan_project_alt` alias.
- ✅ **Phase B — Consolidation**: Unified `metadata.txt` parsing in
  `gis_utils.parse_metadata_content`; consolidated the AST name helper into
  `qgis_base.get_node_name`; shared `BaseAnalysesBuilder` constructor;
  removed the legacy delegating wrappers in `builders/dependencies.py` and
  `providers/git_analysis.py`; `metrics_summarizer` now uses `metric_keys`.
- ✅ **Phase C — Facades**: Deleted all 10 deprecated facade packages
  (`patterns_detectors`, `context_builders`, `summarizers`, `qgis_checkers`,
  `security_checkers`, `entry_point_detectors`, `graph`, `checkers`,
  `commands`, `cli_groups`), dropped the duplicate CLI `_cmd` aliases, and
  repointed tests/docs to canonical paths.
- ✅ **Determinism fix**: `fs_tree` fallback now sorts directories (matches the
  `tree` binary), and the golden fixtures were regenerated — the golden test
  was previously environment/readdir-order dependent.

## 🎯 Immediate Next Steps

- [ ] **Semver decision**: the facades were scheduled for removal in v4.0.0 but
  were removed at 3.5.x. Bump to **4.0.0** (or document the breaking change) on
  the next release.
- [ ] Run `uv run python scripts/sync_metrics.py` to snapshot the new baseline.
- [ ] Apply `scripts/memory_prune.py --apply` to prune expired `next_steps`
  snapshots (>90 days).
- [ ] Register the `@architect` / `@qa_engineer` / `@auditor` subagents in your
  opencode client (declared in `opencode.json`).

## 📋 Future Enhancements

- [ ] Optional follow-up cleanup: collapse the `X.py` + `X_rules.py` split in
  `visitors/` where it is not adding value.
- [ ] Retire the dead `CheckerRegistry` chain (`visitors/security_checker.py`,
  `tech_debt_checker.py`, `optimization_checker.py`, `checker_registry.py`,
  `debt.py`) once its test-only consumers are migrated.
- [ ] Performance profiling on large projects (10k+ files).
- [ ] CI/CD release automation (PyPI upload from GitHub Actions).
- [ ] Custom rule engine (user-defined AST patterns).

## 🐛 Known Issues

**None blocking** — 303 tests passing locally and in Docker; `ai-ctx audit`
PASS (score 90.4); `validate_agent_system.py` PASS.

Note: the `ai-ctx Quality Score` is a heuristic, average-based metric. Removing
small high-maintainability shim files lowered it from 100 to ~90 without a real
quality regression; the release gate is 70.

## 🔧 Technical Debt

- `ruff format --check` reports ~81 pre-existing unformatted files caused by a
  ruff version drift (unrelated to this session).
- Continue improving type hints across all modules.

---

**Session Status:** ✅ Complete — redundancy cleanup (Phases A–C) delivered.
