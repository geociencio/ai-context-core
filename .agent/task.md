# Active Tasks — ai-context-core

This task board tracks the current development phase. Reference plan: `docs/maintenance/redundancy_optimization_plan.md`.

## Phase: Redundancy Cleanup (Phases A–C)

- [x] **Phase A** — Remove dead modules and duplicate symbols (legacy, orchestrator, scorer, graph_engine, engine_config, broken script) <!-- id: rc.a -->
- [x] **Phase B** — Consolidate duplicated helpers and legacy wrappers (metadata parsing, AST name helper, builder bases, metric keys) <!-- id: rc.b -->
- [x] **Phase C** — Remove the 10 deprecated facade packages, CLI alias duplication, and stale references <!-- id: rc.c -->

## Completed (recent)

- [x] Metric key contract unification (canonical `metric_keys.py`)
- [x] `# no-i18n` opt-out + punctuation heuristic
- [x] Observer signal detection hardening + safe dict access
- [x] Regression tests for patterns and `_match_path`
- [x] Metric labels renamed + documented vs `qgis-analyzer`
- [x] Agentic System Migration to Generation 8

## Operational Status

- **Active Phase**: None (redundancy cleanup completed)
- **Current Metrics**: Tests 303/303 passing; `ai-ctx audit` PASS (score 90.4)

