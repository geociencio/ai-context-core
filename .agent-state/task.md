# Active Tasks — ai-context-core

This task board tracks the current development phase.

## Phase: v5.1.0 — Context Alignment & Hardening (P0–P4) — ✅ COMPLETE

Plan: `docs/plans/implementation_plan_v5.1_alignment_hardening.md` (ia-critic PASSED).

- [x] **P0** — AGENTS.md/skills alignment + `analyzer_command` doc <!-- id: v51.p0 -->
- [x] **P1** — token defaults + `[context].mermaid_style` (WS-3) <!-- id: v51.p1 -->
- [x] **P2** — retire domain keys + external regression (WS-4/5) <!-- id: v51.p2 -->
- [x] **P3** — `# noqa: F401` detector + docs + `ai-ctx init` (WS-6/7/8) <!-- id: v51.p3 -->
- [x] **P4** — release v5.1.0 (3 version sites, CHANGELOG, notes, build, tag, GitHub) <!-- id: v51.p4 -->
- [ ] **PyPI v5.1.0** — manual (maintainer): `uv run twine upload dist/*` <!-- id: v51.pypi -->

**Cross-repo**: agentic-forge `release-package` config-driven proposal —
`docs/maintenance/agentic_forge_release_package_proposal.md`.

## Phase: v5.0.0 — Context-Only Contract (F0–F5)

Plan: `docs/plans/implementation_plan_ai_context_core_context_only_v5.md`.
Review: `docs/reviews/ia_critic_implementation_plan_context_only_v5.md`.
ADR: `docs/adr/0008-context-only-contract.md`.

- [x] **F0** — contract & freeze (ADR-0008; `REMOVAL_VERSION=5.0.0`; docs naming) <!-- id: v5.f0 -->
- [x] **F1** — `sources/` + `model/`; `--source`; `context` primary path <!-- id: v5.f1 -->
- [x] **F2** — removal (v5.0.0): commands/visitors/builders; facades; tests <!-- id: v5.f2 -->
- [x] **F3** — token budget + manifest <!-- id: v5.f3 -->
- [x] **F4** — verify + symbol index + health <!-- id: v5.f4 -->
- [ ] **F5** — ecosystem alignment — ⏸ **deferred to sibling repos** (agentic-forge / qgis-plugin-analyzer / sec_interp) <!-- id: v5.f5 -->
- [x] **Release v5.0.0** — version sync + build + `twine check` + tag + GitHub release + **PyPI** <!-- id: v5.rel -->
- [x] **Release v5.0.1** — post-release cleanup (audit P0–P4); tag + GitHub + **PyPI** <!-- id: v501.rel -->

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

- **Active Phase**: None — v5.1.0 released (GitHub); PyPI upload manual (pending)
- **Current Metrics**: Package 205/205 tests; framework 37/37 tests; ruff
  check+format clean; quality 94.7
- **Pending**: PyPI v5.1.0 (maintainer); sibling `agentic-forge` v1.4.2 rollout
  (`sec_interp`; `qgis-plugin-manager` needs local-fork reconciliation)
- **Known**: `forge.py metrics validate` is green after v1.3.0/v1.4.0; the
  framework now has tests and CI.
