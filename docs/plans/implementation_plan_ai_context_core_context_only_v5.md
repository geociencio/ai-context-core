# Implementation Plan: ai-context-core as a Context-Only Tool (v5.0.0)

**Status**: 📋 PROPOSED — awaiting approval to start F0
**Created**: 2026-10-08
**Owner**: @architect (+ @auditor for scope discipline, @qa_engineer for verification)
**Target repo**: `~/qgispluginsdev/ai-context-core` (PyPI `ai-context-core`)
**Consumer impacted**: `sec_interp` (and, as dev-dep, `qgis-plugin-analyzer`)
**Relates to**: `implementation_plan_unify_agentic_systems.md`, session `2026-10-08_ai_context_core_v411.md`

---

## 0. Context

`ai-context-core` (CLI `ai-ctx`, v4.1.1) advertises itself as *"the central nervous
system for your AI-assisted coding workflow"* with **Context Management** as its core
capability. In practice it has grown into a **full static-analysis engine** that
duplicates `qgis-plugin-analyzer` almost line by line.

This plan restores coherence: `ai-context-core` becomes a **context compiler** that
*consumes* analysis (rather than owning it) and produces token-efficient, versioned,
verifiable context artifacts for AI agents.

### Decisions already taken (2026-10-08)

| Decision | Choice |
| :--- | :--- |
| Target identity | **Context-only estricto** (breaking, v5.0.0) |
| Quality Score / `audit` gate | **Renamed to `context health`**, no quality gate |
| First-iteration additions | **Analyzer source · Token budget · verify/staleness · Symbol index** (MCP deferred) |

### Non-goals (owned by siblings)

- QGIS compliance, metadata, Qt6 rules, Processing detection → `qgis-plugin-analyzer`
- i18n AST audit (`MISSING_I18N`) → `qgis-plugin-analyzer`
- Security scanning (Bandit-style, secrets, injection) → `qgis-plugin-analyzer` + `bandit`/`detect-secrets`
- Code-quality scoring / CC gate / module stability → `qgis-plugin-analyzer`
- Lint/format → `ruff`
- Packaging / deploy → `qgis-plugin-manager`
- Code scaffolding → `agentic-forge` / `qgis-plugin-analyzer`

---

## 1. Evidence — what ai-context-core is today

| Signal | Finding |
| :--- | :--- |
| Name / tagline | "AI context" + "Context Management" |
| Actual weight | `analyzer/visitors/` = **58 modules** (`*.py`): security (`injection*`, `secrets`, `insecure_calls`, `ast_security`), QGIS (`qgis_*`, `ast_qgis`), i18n (`i18n*`), design patterns (`singleton/factory/observer/strategy/decorator`), anti-patterns (`god_object`, `spaghetti_code`, `magic_number`), metrics (`halstead`, `complexity_visitor`), plus **33 builder modules** including `aggregator_qgis`, `qgis*`, `security_severity`, `issues`, `patterns`. |
| Context layer | `context/` = **260 LOC** (`manager.py` 59 + `components/` 135 + `components/store_components/` 66). It is **instantiated but not consumed**: `engine.py:22,63` constructs `AIContextManager`, yet no result is ever read; it builds GPT/DeepSeek/Claude *prompts*, disconnected from `AI_CONTEXT.md` generation (which uses `builders/ai_context_generator.py`). |
| Runtime deps | `click`, `rich` only → fully self-contained ⇒ re-implements the analyzer instead of consuming it. |
| Overlap | i18n, Qt6, metadata, security, CC gate, graph/coupling, `serve`, `fix`, `init`, `project_context.json` all duplicated from `qgis-plugin-analyzer`. |
| Root cause | ADR-0002 ("13 improvements") doubled down on *adding analysis* rather than sharpening the context promise. |
| Deprecation debt | `deprecations.py:6` is `REMOVAL_VERSION = "4.0.0"` (already expired vs. v4.1.1); v5.0.0 is the correct target. |

---

## 2. Target contract

> **ai-context-core compiles context.** `source` (extract) → `transform`
> (context / symbol index / budget) → `render` (artifacts) → `verify`.

It is a **consumer** of analysis. Its artifacts are:
**token-efficient**, **versioned**, **verifiable**, and carry **provenance**.

> **Namespace resolution.** The extraction layer is named **`sources/`** —
> *not* `providers/` — to avoid colliding with the existing
> `analyzer/providers/` package (fs cache, scanner, worker, git, config loader,
> `secrets_scanner`). The protocol lives in `sources/base.py` and may retain the
> name `AnalysisProvider` for continuity.

```
src/ai_context_core/
├── sources/            # NEW: external (qgis-analyzer) + builtin (minimal AST)
│   ├── base.py         # AnalysisProvider protocol → model/AnalysisResult
│   ├── external/       # qgis-analyzer adapter
│   └── builtin/        # python-generic AST fallback
├── model/              # NEW: AnalysisResult, SymbolIndex (versioned schema)
├── context/            # transform, budget, verify, store
├── render/             # AI_CONTEXT.md, project_context.json, *.mmd, symbols.json
└── cli/commands/       # slimmed
```

### 2.1 Artifact ownership (`project_context.json`)

Two tools must not write the same filename. Ownership split (fixed in ADR-0008):

| Artifact | Owner | Location |
| :--- | :--- | :--- |
| Analyzer output `project_context.json` | `qgis-plugin-analyzer` | `<project>/analysis_results/project_context.json` |
| Context artifact `project_context.json` | `ai-context-core` | repo root (back-compat); gains `_meta.schema` + `_meta.producer` |

`ai-context-core` consumes the analyzer file as `sources/external` input and
**never** writes into `analysis_results/`. The consumed schema is versioned and
published as part of ADR-0008.

---

## 3. REMOVE (v5.0.0, one deprecation cycle)

### 3.1 CLI commands (`src/ai_context_core/cli/commands/`)

| Delete | Lives in | Rationale |
| :--- | :--- | :--- |
| `audit` | `analysis.py` | Quality gate → analyzer; replaced by `health` |
| `inspect` | `analysis.py` | Single-file deep analysis → analyzer |
| `patterns` | `reports.py` | Design-pattern detection, not context |
| `security` | `reports.py` | → analyzer + bandit |
| `qgis` | `specialized.py` | QGIS compliance/i18n/Qt6 → analyzer |
| `full-scan` | `workflows.py` | Orchestrates removed `audit` + `qgis.check_compliance` (`workflows.py:34,60`); superseded by `context` |
| `fix` | `maintenance.py` | Auto-remediation → analyzer |
| `scaffold` | `maintenance.py` | Code generation → agentic-forge |
| `doctor` | `maintenance.py` | Generic env diagnostics → replaced by `health` |
| `interactive` | `interactive.py` | Not context |
| `serve` | `base.py` | Keep **only** if it serves the *context* report; drop the analysis dashboard |
| `report.py` | `commands/report.py` | Reachable via `reports.py` but **not registered** in `commands/__init__.py`; dead entry point |

**Keep**: `init`, `profiles`, `stats`, `clean`, `analyze`, `context`,
`help-me`, `deps`, `git`, `graph`, `compare`, `roadmap`, **+ new** `verify`, `symbols`, `health`.

> **Contradiction resolved — `help-me`.** Today `help-me` →
> `report.show_specific(..., "recommendations")`
> (`cli/commands/reports.py:25`) → `builders/ai_recommendations.py`, which reads
> `metric_keys.QUALITY_SCORE` (line 45) plus security/pattern data. In v5.0.0 it
> must surface **context recommendations only** (staleness, oversized sections,
> missing provenance), sourced from the new `context/` layer;
> `ai_recommendations.py` is deleted with the quality surface.

### 3.2 Visitors (`analyzer/visitors/`)

The worker injects detectors through `analyzer/registry.py` (`worker.py:132`
imports `antipatterns, issues, patterns, ast_qgis`). Removing a detector module
must also remove its `@register_detector` entry and its key from the aggregation
output.

**Delete** (analysis domains):
- QGIS: `qgis_api`, `qgis_base`, `qgis_visitor`, `ast_qgis`
- i18n: `i18n`, `i18n_components`
- Security: `injection`, `injection_os`, `injection_sql`, `insecure_calls`,
  `secrets`, `security_base`, `ast_security`
- Design patterns: `singleton*`, `factory`, `observer*`, `strategy*`,
  `decorator*`, `patterns`, `patterns_visitor`, `pattern_base`, `frameworks`,
  `framework_rules`
- Anti-patterns: `god_object`, `spaghetti_code`, `magic_number`, `antipatterns`,
  `antipattern_base` — see §10 Q1 (demote vs. delete)
- Metrics/helpers: `halstead`, `checker_base`, `optimizations`,
  `optimization_checker`

**Keep** (structural/context extraction):
`imports`, `imports_visitor`, `import_export`, `ast_visitors`, `sloc`,
`sloc_helpers`, `complexity_visitor`, `classes`, `functions`, `ast_utils`,
`ast_metrics`, `ast_entry_points`, `entry_point_base`, `visitors_base`,
`dead_code`, `docstrings`, `logic`, `exceptions`, `issues`.

> **`issues.py` is dual-use.** `builders/aggregator.py:101,178` calls
> `find_optimizations` (keep) **and** `find_secrets` (delete with security).
> It also registers the `ast_security` detector. **Split the module** (keep
> `find_optimizations`; move `find_secrets` + the `ast_security` registration out)
> rather than deleting it wholesale.

### 3.3 Builders (`analyzer/builders/`)

**Delete**: `aggregator_qgis`, `qgis.py`, `qgis_processing`, `qgis_scope`,
`qgis_summarizer`, `security_severity`, `patterns`, `git_patterns`,
`ai_recommendations`, `html_builder`, `unused_imports`.

**Keep**: `ai_context_generator`, `aggregator`, `context_metrics`, `context_base`,
`structure`, `dependencies`, `cycle_detector`, `formatter`, `reporting`,
`summary_generator`, `summarizer_base`, `metrics_summarizer`, `calculator`,
`git_tech`, `metric_keys`, `parser`, `classifier`, `algorithms`, `builder`,
`builder_components`, `builders_base`, `issues`.

> **Contradiction resolved — `issues` / `summary_generator`.** The prior revision
> deleted `issues` while keeping `summary_generator`, but `IssuesSummarizer` is
> consumed by `ProjectSummaryGenerator` (`summary_generator.py:34`, rendered at
> lines 98–100). **`issues` stays**, trimmed to the sections that survive (drop
> the security/quality feeds); `summary_generator` stays.
>
> **Contradiction resolved — `patterns` builder.** `PatternsBuilder`
> (`builders/patterns.py`) is a live `ai_context_generator.py:42,51` section, and
> the `patterns` output key is produced by `aggregator._aggregate_patterns`
> (line 113) from the `patterns` visitor detector. Removing the design-pattern
> domain therefore requires: drop `patterns` from `AIContextGenerator`'s
> `DEFAULT_SECTIONS` / `_builder_classes`, and remove the `patterns` key and
> `_aggregate_patterns` from `aggregator.py`.
>
> **`aggregator.py` / `builder.py` are load-bearing** (orchestration + import
> graph) and were missing from the earlier keep list.

### 3.4 Config

- Delete `config/profiles/qgis.toml` (the only shipped profile file). The
  `python-generic` default is **not** a file — it is the built-in defaults in
  `analyzer/providers/config_loader.py`; keep it and add the new
  `[sources]` / `[context.budget]` keys there.
- `deprecations.py`: set `REMOVAL_VERSION = "5.0.0"` (currently `"4.0.0"`); add
  facades for removed imports for one cycle.

---

## 4. ADD (first iteration)

### A. Source layer (keystone) — `sources/`
- `sources/base.py`: `AnalysisProvider` protocol → normalized `model/AnalysisResult`.
- `sources/external/qgis_analyzer.py`: run `qgis-analyzer analyze . --json` or read
  `analysis_results/project_context.json`.
- `sources/builtin/`: minimal `python-generic` AST extraction (structure, imports,
  complexity) as a standalone fallback.
- Config `[sources] source = "auto|external|builtin"`; `--source` flag on `analyze`/`context`.
- Default `auto`: external if analyzer output/dep present, else builtin.
- The builtin source must also supply the data `roadmap` needs (complexity + churn);
  churn continues to come from the retained `analyzer/providers/git_churn.py`.

### B. Token budget
- `context/budget.py`: estimator (heuristic `chars/4`; `tiktoken` as optional extra).
- `[context.budget]` per-section limits; `--max-tokens`.
- Render a summary: `context: 3,412 / 8,000 tokens (43%)`; per-section counts in the manifest.

### C. verify / staleness
- `context/verify.py` + command `verify`.
- Every artifact carries `_meta` = `{schema, tool_version, git_sha, content_hash}` — reuse
  the 4.1.1 cache-versioning pattern.
- `ai-ctx verify` exits `1` on drift; `ai-ctx context --check` for CI.

### D. Symbol index
- `context/symbol_index.py` + command `symbols`.
- AST extraction of definitions (module/class/function/method) + references with `file:line`.
- Emits versioned `symbols.json`; query via `--grep`.

### E. context health (ex-Quality Score)
- Command `health`: freshness + symbol coverage + token size + provenance.
- **No quality gate.** Exit code non-zero only for staleness failures.

---

## 5. Phased execution

### F0 — Contract & freeze
- Write `docs/adr/0008-context-only-contract.md` (accepted decision).
- Bump `REMOVAL_VERSION` to `5.0.0`; freeze new analysis features.
- Rename score surface to "context health" in docs.
- **Exit**: ADR merged; no code removal yet.

### F1 — Source layer
**Status**: ✅ COMPLETED (2026-10-09) — `model/AnalysisResult`, `sources/{base,builtin,external,pipeline}`, `--source` on `analyze`/`context`, `engine.collect()`; tests 333 → 349; external verified against real `sec_interp` output.
- Implement `sources/` + `model/`; wire `--source`; make `context` the primary path.
- **Prerequisite**: provision `qgis-plugin-analyzer` + the `sec_interp` checkout (or a
  local fixture) for the external-vs-builtin regression; record if a fixture is substituted.
- **Exit**: `ai-ctx context` on `sec_interp` produces equivalent sections via external
  source vs. builtin (regression snapshot diff); `pytest` green.

### F2 — Removal (v5.0.0)
- Delete §3 files/commands; add deprecation facades; update `README.md`, `CONFIGURATION.md`,
  `.analyzerignore` semantics; prune tests.
- Update `AIContextGenerator.DEFAULT_SECTIONS` / `_builder_classes` (drop `patterns`,
  `qgis`) and `aggregator` output keys (`patterns`, `qgis_compliance`, `security`);
  split `visitors/issues.py` (keep `find_optimizations`, drop `find_secrets` +
  `ast_security`).
- **Exit**: `ai-ctx --help` shows only the context surface; `pytest` green with the
  **measured** post-removal count recorded per §9; golden fixtures regenerated and
  reviewed; `ruff check` clean.

### F3 — Token budget + manifest
- Implement §4B; add manifest (`context_manifest.json`) with per-section token counts.
- **Exit**: `context --max-tokens` truncates deterministically; manifest matches rendered sizes.

### F4 — verify + symbol index + health
- Implement §4C/§4D/§4E.
- **Exit**: `verify` returns 0 after fresh `context`, 1 after editing a tracked file;
  `symbols --grep` returns `file:line`.

### F5 — Ecosystem alignment
- Cross-link READMEs (`qgis-plugin-analyzer` ↔ `ai-context-core`).
- Update `agentic-forge` skill `project-context` references.
- Update SecInterp workflows (`/start-session`, `/close-session`) and docs referencing
  `ai-ctx qgis`/`audit` → `qgis-analyzer` + `ai-ctx context`.

---

## 6. Migration & deprecation

- **Major bump** `4.x → 5.0.0`; one deprecation cycle for removed imports (warn, don't break).
- Removed CLI commands: keep hidden no-op stubs that print a redirect pointer to the
  owner (`qgis-analyzer …` / `agentic-forge …`) for one release.
- `project_context.json`: keep the root path for back-compat and add a
  `_meta = {schema, producer, tool_version}` block (§2.1); the analyzer file under
  `analysis_results/` is a distinct, versioned contract owned by `qgis-plugin-analyzer`.
- Changelog: `### Removed` + `### Changed` with the identity contract.

## 7. Ecosystem impact

| Consumer | Impact |
| :--- | :--- |
| `sec_interp` | No runtime breakage. Already uses `qgis-analyzer` for i18n/CC gates. Workflows referencing `ai-ctx qgis`/`audit` must switch to `qgis-analyzer` + `ai-ctx context`; `pyproject` stays (uses `context`/`roadmap`/`git`). Resolves the i18n inconsistency (F6) by single-sourcing. |
| `qgis-plugin-analyzer` | Becomes sole owner of hygiene; uses `ai-context-core` as dev-dep → must follow the deprecation cycle. Publish a stable `project_context.json` schema contract. |
| `agentic-forge` | Update `project-context` skill to describe the new division. |

## 8. Risks & mitigations

| Risk | Mitigation |
| :--- | :--- |
| `roadmap` needs complexity + churn | **Do not** prune `complexity_visitor`, `sloc`, `git_tech`. |
| `tiktoken` adds a dependency | Optional extra with heuristic fallback. |
| Breaking API for the analyzer (dev-dep) | Mandatory one-cycle deprecation + redirect stubs. |
| Loss of standalone (non-QGIS) use | Keep minimal `sources/builtin` for `python-generic`. |
| Scope creep during F2 | @auditor gate: any re-added analysis feature is rejected. |

## 9. Verification

- **Per phase**: `uv run pytest -q` + `uv run ruff check .` in `ai-context-core`.
- **Test-count target (F2)**: baseline is **333** (v4.1.1). Removing the security,
  QGIS, i18n and design-pattern domains plus their coverage tests will drop this
  substantially. **Measure and record the exact post-F2 count in this plan** —
  the working estimate is **~180–220**; do not assert a fixed number until
  `pytest --collect-only -q | tail -1` confirms it.
- **Golden fixtures (F2)**: regenerate `tests/fixtures/golden_expected/`
  (`tests/test_golden_reports.py`) after `AIContextGenerator`'s section set and
  `aggregator` output keys change; review the diff for removed sections rather
  than blind-accepting.
- **Regression (F1)**: snapshot `AI_CONTEXT.md` / `project_context.json` on
  `sec_interp` with `--source external` vs `builtin`; sections must match modulo
  provider provenance.
  **Precondition**: this requires `qgis-plugin-analyzer` installed and the
  `sec_interp` checkout available. Neither exists in the default dev/CI
  environment — the F1 exit must explicitly provision them or substitute a local
  fixture, and this must be stated as a prerequisite, not assumed.
- **CLI regression**: assert `full-scan`, `help-me` and `report.py` no longer
  break (removed / re-scoped per §3.1).
- **Staleness**: `ai-ctx verify` → 0 fresh, 1 stale.
- **Budget**: `--max-tokens N` never exceeds `N`; manifest sums equal rendered counts.
- **Cross-repo**: after F5, `forge validate` green in the three sibling repos.

## 10. Open questions

> **Resolved during the 2026-10-09 `/ia-critic` review** (see
> `docs/reviews/ia_critic_implementation_plan_context_only_v5.md`): the
> `issues`/`summary_generator`, `patterns`/`ai_context_generator`, `full-scan`,
> `help-me`/`ai_recommendations` contradictions; the `providers/` namespace
> collision; the `secrets_scanner` location; and the `project_context.json`
> ownership split.

1. Anti-patterns: demote to context warnings or delete entirely in F2?
2. `compare`: keep as *context delta* tool, or delegate diffing to CI snapshots?
3. `serve`: keep a context-only HTML view, or drop HTML entirely (analyzer owns dashboards)?
4. Should `dependency graph` (`deps`) stay in ai-context-core, or delegate to
   `qgis-analyzer graph` and keep only the Mermaid render for context?

---

## Appendix A — CLI surface before/after

| Command | 4.1.1 | 5.0.0 |
| :--- | :---: | :---: |
| `analyze` | ✅ | ✅ (source-backed) |
| `context` | ✅ | ✅ (primary) |
| `deps` / `graph` | ✅ | ✅ (see Q4) |
| `git` / `roadmap` | ✅ | ✅ |
| `stats` / `compare` | ✅ | ✅ |
| `help-me` | ✅ | ✅ (context recommendations only) |
| `init` / `profiles` / `clean` | ✅ | ✅ |
| `verify` / `symbols` / `health` | ❌ | ✅ **new** |
| `audit` / `inspect` | ✅ | ❌ (→ analyzer / `health`) |
| `full-scan` | ✅ | ❌ (superseded by `context`) |
| `qgis` / `security` / `patterns` | ✅ | ❌ (→ analyzer) |
| `fix` / `scaffold` / `doctor` | ✅ | ❌ (→ analyzer / agentic-forge / `health`) |
| `interactive` / `serve` | ✅ | ❌ (see Q3) |
