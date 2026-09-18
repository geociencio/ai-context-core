# Maintenance Session: 2026-09-17 - Corrections & Agentic System Gen 8

## Technical Summary

Two bodies of work were completed on `ai-context-core`:

1. **Corrections from `developer_recommendations.md`**: consolidated the outstanding recommendations (#2 metric key contract, #6 i18n precision, hardening, #7 regression tests, #8 metric clarity) into implementable items and shipped them.
2. **Agentic system migration to Generation 8**: adopted the opencode-native architecture from `qgis-plugin-analyzer` (root `AGENTS.md` as SSoT, native subagents, consolidated scripts, 3-tier memory), in English with 3 subagents and ruff-only quality gates.

## Changes Made

### Analyzer corrections
- **`builders/metric_keys.py`** (new): canonical metric key constants + `missing_metric_keys`.
- **`builders/calculator.py`**: removed duplicate alias keys (`avg_complexity`, `avg_maintainability`), now uses constants.
- **`builders/formatter.py`, `metrics_summarizer.py`, `aggregator.py`**: aligned to canonical keys; added missing-key validation.
- **`visitors/i18n_components.py`, `i18n.py`, `logic.py`, `qgis_visitor.py`, `providers/worker.py`**: `# no-i18n` opt-out via tokenize line mapping; punctuation heuristic.
- **`visitors/observer_rules.py`**: exact `pyqtSignal`/`Signal` matching (no substring false positives).
- **`builders/issues.py`, `patterns.py`, `summary_generator.py`, `git_patterns.py`**: safe `.get()` access.
- **Metric labels renamed** across CLI/builders to `ai-ctx Quality Score` and `Avg Cyclomatic Complexity`.

### Agentic system (Gen 8)
- Root `AGENTS.md`, `opencode.json`, `.agent/AGENTS.md` pointer.
- `scripts/validate_agent_system.py`, `memory_prune.py`, `sync_metrics.py`; retired `skill_sync.py`.
- Memory: `memory_policy.md`, `agent_metrics.json`, YAML `AGENT_LESSONS.md`, `task.md`.
- 14 skills (6 adapted, 8 new), 11 workflows + `index.md`, `.agent/README.md` + `QUICK_REFERENCE.md`.

### Tests
- `tests/test_metric_keys.py`, `tests/test_i18n_opt_out.py`, `tests/test_regression_patterns.py` (new).
- Updated `tests/test_cli.py`, `tests/test_visualization.py`, `tests/test_absolute_final.py`, `tests/test_coverage_boost.py`.

## Verification Results

- `uv run pytest -q`: **286 passed**.
- `uv run ruff check .`: clean.
- `uv run python scripts/validate_agent_system.py`: **PASS** (14 skills, 11 workflows).

## Impact

- Metric contract is now single-source (no silent `0` fallbacks from key mismatches).
- i18n counting supports explicit developer opt-out, reducing false positives.
- The agentic tooling is now opencode-native, eliminating the runtime bridge and enabling consistent, validated skills/workflows.
