# Active Tasks — ai-context-core

This task board tracks the current development phase.

## Phase: Deep Cleanup & v4.0.0 Release

- [x] **Anti-patterns surfaced** — aggregate and render anti-pattern detections <!-- id: dc.ap -->
- [x] **Dead code removal** — retire `CheckerRegistry` chain + facades <!-- id: dc.dead -->
- [x] **Architecture purity** — move `secrets_scanner` to providers <!-- id: dc.pure -->
- [x] **Metric key contract** — enforce `metric_keys` in CLI/builders <!-- id: dc.mk -->
- [x] **Hygiene** — `ruff format`, remove legacy wrappers + re-export hop <!-- id: dc.hyg -->
- [x] **Release v4.0.0** — tag + GitHub release (PyPI manual pending) <!-- id: dc.rel -->

## Completed (recent)

- [x] Redundancy cleanup (Phases A–C)
- [x] Metric key contract unification (canonical `metric_keys.py`)
- [x] Agentic System Migration to Generation 8

## Operational Status

- **Active Phase**: None (deep cleanup + v4.0.0 release completed)
- **Current Metrics**: Tests 299/299 passing; `ai-ctx audit` PASS (score 90.7)
- **Pending**: PyPI upload (manual)
