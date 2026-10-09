# AI Critic — Implementation Plan Audit

**Reviewed plan**: [`docs/plans/implementation_plan_ai_context_core_context_only_v5.md`](../plans/implementation_plan_ai_context_core_context_only_v5.md)
**Workflow**: `/ia-critic` (`.agent/workflows/ia-critic.md`)
**Date**: 2026-10-09
**Reviewer**: @auditor (Hallucination Hunter)
**Verdict**: ❌ **FAILED — revisions required before F2** → ✅ **RESOLVED 2026-10-09**
**F0 status**: ⚠️ conditionally approvable **after** the corrections below are folded into ADR-0008.

> **Resolution status (2026-10-09).** All §6 required corrections were applied to
> the plan in place: §1 evidence corrected, `sources/` namespace adopted,
> artifact-ownership split added (§2.1), contradictions resolved (§2/§3.1/§3.3),
> keep/delete inventory completed (§3.2/§3.3), and verification extended (§9).
> The four blocking contradictions are closed; the review remains as the audit
> record.

> Directionally sound: the context-only identity is coherent and the keep/remove
> taxonomy is mostly accurate. However, the plan contains factual drift, one
> direct internal contradiction, and several unaddressed breakages that would
> surface during F2.

Context loaded: `.agent-state/memory/AGENT_LESSONS.md` (metric-key contract,
module-split complexity budget, generated-artifact hygiene).

---

## 1. Ground-truth corrections (§1 Evidence)

| Plan claim | Reality | Severity |
| :--- | :--- | :--- |
| `visitors/` ≈ **55** modules | **58** `*.py` under `analyzer/visitors/` | minor |
| `context/` = **~194 LOC** | **260 LOC** (`manager` 59 + `components` 135 + `store_components` 66) | minor |
| `context/` is "legacy/**unused**" | Instantiated but never consumed: `analyzer/engine.py:22,63` (`self.context_manager = AIContextManager(...)`, no other usage) | wording — conclusion holds, evidence overstated |
| Runtime deps = `click`, `rich` | ✅ confirmed (`pyproject.toml:25-28`) | — |
| `providers/` = "**NEW**" | **Collision**: `analyzer/providers/` already exists (`fs_cache`, `worker`, `git_churn`, `config_loader`, `gis_utils`, `secrets_scanner`, …) | documented §3 |
| ADR target `0008` | ✅ next free number (`docs/adr/` ends at `0007`) | — |
| `REMOVAL_VERSION` bump to `5.0.0` | Correct, but current value is `"4.0.0"` (`deprecations.py:6`) — already expired vs. 4.1.1 | note the pre-existing debt |

---

## 2. Blocking contradictions (must fix)

### 2.1 Delete `builders/issues.py` breaks `summary_generator`
`IssuesSummarizer` is consumed by `ProjectSummaryGenerator`
(`builders/summary_generator.py:34`, used for `CRITICAL ISSUES` /
`MAIN RECOMMENDATIONS` at lines 98–100), which is itself wired at
`builders/reporting.py:134-136`. §3.3 deletes `issues` while keeping
`summary_generator` → **internal inconsistency**.

### 2.2 Delete `builders/patterns.py` breaks AI_CONTEXT generation
`PatternsBuilder` is registered as a rendered section in
`builders/ai_context_generator.py:42,51` and exported from
`builders/__init__.py:19`. §10 Q1 discusses only *anti*-patterns; the
design-pattern builder wiring is unaddressed.

### 2.3 `full-scan` is kept but is un-buildable
`cli/commands/workflows.py` calls `analyze.run_audit` (line 34, removed) and
`qgis.check_compliance` (line 60, removed). Keeping `full-scan` in Appendix A
requires a rewrite that the plan does not describe.

### 2.4 `help-me` is kept but its data source is removed
`help-me` → `report.show_specific(..., "recommendations")`
(`cli/commands/reports.py:25`) → `builders/ai_recommendations.py` reads
`metric_keys.QUALITY_SCORE` (line 45). `ai_recommendations` appears in **neither**
the keep nor the delete list.

---

## 3. Scope / architecture gaps

- **Provider namespace collision.** The target tree (§2) removes `analyzer/`
  entirely and adds a top-level `providers/`, a far larger restructure than §3
  states. Choose and document a namespace (e.g.
  `analyzer/providers/{external,builtin}` or a new `context_providers/`).
- **Keep/delete inventory incomplete.** No disposition given for:
  - visitors: `antipatterns`, `antipattern_base`, `ast_*`, `docstrings`, `issues`,
    `logic`, `optimizations`, `optimization_checker`, `pattern_base`, `patterns`,
    `patterns_visitor`, `sloc_helpers`;
  - builders: `aggregator`, `ai_recommendations`, `builder`, `builder_components`,
    `builders_base`, `html_builder`, `parser`, `summary_generator`,
    `unused_imports`;
  - CLI: `report.py`, `workflows.py`, `analyze.py`.
- **Stale path.** `secrets_scanner.py` lives in `analyzer/providers/`, not
  `visitors/` (moved in v4.0.0) — §3.2 is stale on this item.
- **`project_context.json` ownership is circular.** `qgis-analyzer` produces one
  and `ai-context-core` also writes one. The ADR must define filenames/dirs
  (`analysis_results/` vs. repository root) and the schema contract.
- **Dead CLI entry point.** `cli/commands/report.py` is reachable via `reports.py`
  but is **not registered** in `cli/commands/__init__.py`; it needs an explicit
  disposition.
- **Hygiene bug surfaced (independent).** Generated artifacts are committed under
  `src/ai_context_core/cli/` (`AI_CONTEXT.md`, `PROJECT_SUMMARY.md`,
  `project_context.json`, `.ai_context_cache.json`). Should be cleaned.

---

## 4. Verification-plan gaps (§9)

- Snapshot regression on `sec_interp` with `--source external` requires
  `qgis-analyzer` **and** that repository to be present; neither is guaranteed in
  this environment/CI.
- No target test count or golden-fixture regeneration step for the F2 removal
  (plan only states "expected count reduced from 333").
- `full-scan` and `help-me` regressions are not covered.
- `ai-ctx audit` is referenced by external consumers (SecInterp workflows, CI);
  migration must be verified, not merely redirected.

---

## 5. Observations (non-blocking)

- Module-to-command mappings in §3.1 are accurate (`analysis.py`, `reports.py`,
  `specialized.py`, `maintenance.py`, `interactive.py`, `base.py`).
- `roadmap` risk is correctly identified: verified it depends only on complexity
  + churn (`cli/commands/roadmap.py:43-59`) — do **not** prune
  `complexity_visitor`, `sloc`, `git_tech`.
- The `sloc*` keep note is fine (`sloc.py`, `sloc_helpers.py`).
- `context/` is a better fit for *repurposing* (transform/budget/verify/store)
  than deletion; the plan already reflects this.

---

## 6. Required corrections before F2

1. Resolve §2 contradictions: `issues`↔`summary_generator`,
   `patterns`↔`ai_context_generator`, `full-scan`, `help-me`/`ai_recommendations`.
2. Rename the new provider layer to avoid the `analyzer/providers/` collision and
   correct the §2 target tree.
3. Complete the keep/delete inventory and fix the `secrets_scanner` location.
4. Define the `project_context.json` schema/ownership split in ADR-0008.
5. Correct §1 numbers (58 visitors, 260 LOC) and soften "unused" →
   "instantiated but not consumed".
6. Extend §9 with a test-count target, golden-fixture refresh, and explicit
   external-provider availability assumptions.

---

## 7. Sign-off

- **F0** (ADR + freeze, docs-only): may start once §6 items 1, 4, 5 are reflected
  in ADR-0008.
- **F1** (provider layer): blocked on §6 item 2.
- **F2** (removal): blocked on all §6 items.

*Philosophy: it is better to find an error in the blueprint than in the building.*
