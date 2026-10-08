# Maintenance Session: 2026-10-08 — Redundancy Cleanup

Reference plan: [`docs/maintenance/redundancy_optimization_plan.md`](redundancy_optimization_plan.md)

## Technical Summary

Deep redundancy audit followed by a three-phase cleanup (A/B/C) of the
`ai-context-core` codebase. The goal was to remove dead code, consolidate
duplicated logic, and retire the deprecated compatibility facades — without
touching the engine → providers → visitors/builders → reporting architecture.

Net result: 6 dead modules + 10 deprecated facade packages + 33 facade files
removed, several duplicate helpers merged, the CLI de-duplicated, and the
generated reports made deterministic.

## Changes Made

### Phase A — Dead code removal
- Deleted `visitors/legacy.py`, `visitors/antipattern_orchestrator.py`,
  `builders/scorer.py`, `builders/graph_engine.py`, `engine_config.py` and the
  broken `check_complexity.py` script.
- Removed duplicate `HalsteadVisitor` (`ast_metrics.py`), `_mask_secret`,
  `fs_tree.analyze_structure`, `fs_utils.count_file_types`/
  `calculate_size_stats`, and the `scan_project_alt` alias.
- Retired the coverage-only tests that kept this code alive.

### Phase B — Consolidation
- `metadata.txt` parsing unified in `gis_utils.parse_metadata_content`
  (interpolation disabled); `qgis_resources` now delegates to it.
- AST name resolution consolidated into `visitors/qgis_base.get_node_name`.
- Shared `BaseAnalysesBuilder` constructor for `BaseContextBuilder` and
  `BaseSummarizer`.
- Legacy delegating wrappers removed from `builders/dependencies.py` and
  `providers/git_analysis.py`; tests migrated to canonical classes.
- `metrics_summarizer.py` reads metrics via `metric_keys` constants.

### Phase C — Facade removal & determinism
- Deleted the 10 deprecated facade packages: `patterns_detectors`,
  `context_builders`, `summarizers`, `qgis_checkers`, `security_checkers`,
  `entry_point_detectors`, `graph`, `checkers`, `commands`, `cli_groups`.
- Dropped the duplicate CLI `_cmd` aliases in `cli/__init__.py`.
- Replaced `test_deprecated_facades.py` with `test_deprecated_aliases.py`.
- `fs_tree._generate_tree_fallback` now sorts directories (aligning the
  fallback with the `tree` binary), and the golden fixtures were regenerated.

## Verification Results

- `uv run ruff check .` — clean.
- `uv run pytest -q` — **303 passed** (local, Python 3.12).
- `make docker-test` — **303 passed** (Docker, Python 3.11).
- `uv run ai-ctx audit --threshold 70` — PASS (score 90.4).
- `uv run python scripts/validate_agent_system.py` — PASS.

### Note on the quality score
The heuristic `ai-ctx Quality Score` dropped from 100.0 to ~90.4. The removed
facades were tiny modules with a Maintenance Index ≈100; deleting them lowered
the *average* maintainability (60 → 51.9). This is a metric artefact, not a
quality regression — the release gate (70) remains comfortably passed.

### Fixtures / pre-existing issue fixed
`test_golden_reports` was environment-dependent on the host filesystem's
directory read order. Confirmed pre-existing (the parent commit's source fails
against the current fixtures). Made deterministic via directory sorting.

## Impact

- ~1,079 net lines removed across the three cleanup commits.
- Smaller, clearer package surface; no deprecated import paths remain.
- Deterministic golden reports.
- **Breaking change:** deprecated facade import paths were removed ahead of the
  planned v4.0.0 removal — a major version bump is recommended.
