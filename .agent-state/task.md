# Active Tasks — ai-context-core

This task board tracks the current development phase.

## Phase: v4.1.0 — Context Map & Debt Prioritization

Plan: `docs/maintenance/refactoring_plan_v4.1.0.md` (WS-0..WS-5).

- [ ] **WS-0** — unify config loading (canonical `providers.config_loader.load_config`) <!-- id: v41.ws0 -->
- [ ] **WS-1** — repair import graph + mermaid diagram <!-- id: v41.ws1 -->
- [ ] **WS-2** — realistic churn/hotspots (per-file, `--find-renames`) <!-- id: v41.ws2 -->
- [ ] **WS-3** — anti-pattern severity + allowlist + prioritization <!-- id: v41.ws3 -->
- [ ] **WS-4** — context-only mode (`ai-ctx context`, decouple score) <!-- id: v41.ws4 -->
- [ ] **WS-5** — selectable `AI_CONTEXT.md` sections <!-- id: v41.ws5 -->

## Completed (recent)

- [x] Deep cleanup + v4.0.0 release (tag + GitHub release; PyPI manual pending)
- [x] Redundancy cleanup (Phases A–C)
- [x] Metric key contract unification (canonical `metric_keys.py`)
- [x] Agentic System Migration to Generation 8

## Operational Status

- **Active Phase**: v4.1.0 (WS-0 in progress)
- **Current Metrics**: Tests 302/302 passing; `ai-ctx audit` PASS (score 90.8)
- **Pending**: PyPI upload (manual)
