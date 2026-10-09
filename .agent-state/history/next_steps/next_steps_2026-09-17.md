# Next Steps - ai-context-core

**Last Updated:** 2026-09-17

## ✅ Completed in This Session

### Corrections from `developer_recommendations.md`
- ✅ **Metric key contract (#2)**: Introduced `builders/metric_keys.py` with canonical keys, removed duplicate aliases, aligned all consumers, and added `missing_metric_keys` validation.
- ✅ **i18n precision (#6)**: Added `# no-i18n` inline opt-out (tokenize-based) and a punctuation-dominance heuristic in `is_translatable_string`.
- ✅ **Hardening (#1/#3/#4)**: Safe `.get()` access across pattern/report builders; tightened `_is_signal_definition` to exact `pyqtSignal`/`Signal` matching.
- ✅ **Regression tests (#7)**: Added tests for patterns without `class`, `_match_path` recursive globs + Windows paths.
- ✅ **Metric clarity (#8)**: Renamed user-facing labels (`ai-ctx Quality Score`, `Avg Cyclomatic Complexity`) and documented semantics vs `qgis-analyzer` in README.

### Agentic System Migration (Generation 8)
- ✅ Root `AGENTS.md` as SSoT (English) + `opencode.json` with native subagents (architect/qa_engineer/auditor).
- ✅ Retired `skill_sync.py`; added `validate_agent_system.py`, `memory_prune.py`, `sync_metrics.py`.
- ✅ 3-tier memory model (`memory_policy.md`, `agent_metrics.json`, YAML lessons, `task.md`).
- ✅ Expanded to 14 English skills and 11 workflows (`index.md`, README, QUICK_REFERENCE).

## 🎯 Immediate Next Steps

- [ ] Run `uv run python scripts/sync_metrics.py` on the next session start to seed `agent_metrics.json`.
- [ ] Apply `scripts/memory_prune.py --apply` to prune expired `next_steps` snapshots (>90 days).
- [ ] Register the `@architect` / `@qa_engineer` / `@auditor` subagents in your opencode client (they are declared in `opencode.json`).

## 📋 Future Enhancements

- [ ] `--include-md` flag to inject arbitrary Markdown into the architecture section (deferred by decision).
- [ ] Performance profiling on large projects (10k+ files).
- [ ] CI/CD release automation (PyPI upload from GitHub Actions).
- [ ] Custom rule engine (user-defined AST patterns).

## 🐛 Known Issues

**None blocking** — 286 tests passing; `validate_agent_system.py` PASS.

## 🔧 Technical Debt

- Monitor the fragmentation of `*_components` packages; consolidate if they become too sparse.
- Continue improving type hints across all modules.

---

**Session Status:** ✅ Complete — corrections implemented and agentic system migrated to Gen 8.
