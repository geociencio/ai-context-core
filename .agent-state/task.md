# Active Tasks — ai-context-core

This task board tracks the current development phase.

## Phase: v5.0.0 — Context-Only Contract (F0–F5)

Plan: `docs/plans/implementation_plan_ai_context_core_context_only_v5.md`.
Review: `docs/reviews/ia_critic_implementation_plan_context_only_v5.md`.
ADR: `docs/adr/0008-context-only-contract.md`.

- [x] **F0** — contract & freeze (ADR-0008; `REMOVAL_VERSION=5.0.0`; docs naming) <!-- id: v5.f0 -->
- [ ] **F1** — `sources/` + `model/`; `--source`; `context` primary path <!-- id: v5.f1 -->
- [ ] **F2** — removal (v5.0.0): commands/visitors/builders; facades; tests <!-- id: v5.f2 -->
- [ ] **F3** — token budget + manifest <!-- id: v5.f3 -->
- [ ] **F4** — verify + symbol index + health <!-- id: v5.f4 -->
- [ ] **F5** — ecosystem alignment <!-- id: v5.f5 -->

**Feature freeze**: no new analysis capabilities until F2 (@auditor gate).

## Phase: v4.1.1 — Report Correctness Fixes (F1–F5)

Source: `docs/maintenance/improvement_report_v4.1.0.md`.

- [x] **F1** — version + config-fingerprint the analysis cache <!-- id: v411.f1 -->
- [x] **F2** — real security `max_severity` (AST-only + merge) + top-3 indicator <!-- id: v411.f2 -->
- [x] **F3** — `__all__` awareness + `ignore_package_reexports` for `__init__.py` <!-- id: v411.f3 -->
- [x] **F4** — scope git churn to analyzed code (code + `raw_*`) <!-- id: v411.f4 -->
- [x] **F5** — gate the "No Processing Algorithms" note on processing intent <!-- id: v411.f5 -->
- [x] **Release v4.1.1** — tag + GitHub release; PyPI pending credentials <!-- id: v411.rel -->

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

- **Active Phase**: v5.0.0 — Context-Only Contract (F0 done; F1 next)
- **Current Metrics**: Tests 333/333 passing; `ai-ctx audit` PASS (score 90.2)
- **Pending**: F1 source layer (`sources/` + `model/`, `--source`, `context` primary)
- **Known**: 5 `forge.py metrics validate` false positives in `.agent/` framework
  scaffold/generic skills (see `next_steps.md` → Known Issues). Non-blocking.
