# Active Tasks — ai-context-core

This task board tracks the current development phase.

## Phase: v4.1.1 — Report Correctness Fixes (F1–F5)

Source: `docs/maintenance/improvement_report_v4.1.0.md`.

- [x] **F1** — version + config-fingerprint the analysis cache <!-- id: v411.f1 -->
- [x] **F2** — real security `max_severity` (AST-only + merge) + top-3 indicator <!-- id: v411.f2 -->
- [x] **F3** — `__all__` awareness + `ignore_package_reexports` for `__init__.py` <!-- id: v411.f3 -->
- [x] **F4** — scope git churn to analyzed code (code + `raw_*`) <!-- id: v411.f4 -->
- [x] **F5** — gate the "No Processing Algorithms" note on processing intent <!-- id: v411.f5 -->

## Phase: v4.1.0 — Context Map & Debt Prioritization

Plan: `docs/maintenance/refactoring_plan_v4.1.0.md` (WS-0..WS-5).

- [x] **WS-0** — unify config loading (canonical `providers.config_loader.load_config`) <!-- id: v41.ws0 -->
- [x] **WS-1** — repair import graph + mermaid diagram <!-- id: v41.ws1 -->
- [x] **WS-2** — realistic churn/hotspots (per-file, `--find-renames`) <!-- id: v41.ws2 -->
- [x] **WS-3** — anti-pattern severity + allowlist + prioritization <!-- id: v41.ws3 -->
- [x] **WS-4** — context-only mode (`ai-ctx context`, decouple score) <!-- id: v41.ws4 -->
- [x] **WS-5** — selectable `AI_CONTEXT.md` sections <!-- id: v41.ws5 -->
- [x] **Release v4.1.0** — tag + GitHub release + PyPI publish <!-- id: v41.rel -->

## Completed (recent)

- [x] Deep cleanup + v4.0.0 release (tag + GitHub release; PyPI manual pending)
- [x] Redundancy cleanup (Phases A–C)
- [x] Metric key contract unification (canonical `metric_keys.py`)
- [x] Agentic System Migration to Generation 8

## Operational Status

- **Active Phase**: None (v4.1.1 F1–F5 implemented; pending release)
- **Current Metrics**: Tests 333/333 passing; `ai-ctx audit` PASS (score 90.2)
- **Pending**: release v4.1.1 (tag + GitHub + PyPI) when approved
- **Known**: 5 `forge.py metrics validate` false positives in `.agent/` framework
  scaffold/generic skills (see `next_steps.md` → Known Issues). Non-blocking.
