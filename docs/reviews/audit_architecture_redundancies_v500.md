# Architectural Audit — Redundancies, Dead Code & Improvement Recommendations

**Scope**: `ai-context-core` (CLI `ai-ctx`) `v5.0.0` (`main` @ `ddbc955`)
**Type**: Deep static audit (redundancy · dead code · compatibility debt)
**Date**: 2026-10-10
**Reviewer**: @architect (assisted by vulture, coverage, AST reachability)
**Status**: 📋 Findings recorded — remediation not started

---

## 0. Snapshot

| Metric | Value |
| :--- | :--- |
| Modules (`src/ai_context_core`) | 104 |
| Source LOC | 6,718 |
| Tests | 182 passed (`pytest -q`) |
| Coverage | 88% (2,918 stmts, 353 missed) |
| Layer sizes | `builders/` 24 · `visitors/` 19 · `providers/` 18 · `sources/` (new) · `context/` · `model/` |

The P0–P4 cleanup (`e22196f refactor(core): remove divergences and dead code`) already
removed the bulk of the legacy analysis surface. What remains is **one latent v4 render
path**, **expired compatibility facades**, and **residual cruft** — all of which
contradict the v5.0.0 "context-only" contract.

---

## 1. Redundancies

### R1 — Dual render pipeline (highest impact)
Two code paths write the same artifacts.

| Path | Entry | Artifacts |
| :--- | :--- | :--- |
| v5 (target) | `sources/pipeline.py:114` `render_context()` | `AI_CONTEXT.md`, `context_manifest.json`, `project_context.json` |
| v4 (legacy) | `analyzer/engine.py:116` `analyze()` → `_generate_outputs()` (`engine.py:138-172`) | same three files |

The CLI selects per source: `cli/commands/analyze.py:38-61` routes `external` through
`render_context` but `builtin` through `ProjectAnalyzer.analyze()`. The two paths diverge
in **provenance** (the engine path omits `schema` and the `AnalysisResult.with_meta()`
normalization) and in `_ensure_defaults` handling.

`BuiltinSource` already wraps `ProjectAnalyzer.collect()` (side-effect-free), so `analyze`
can use `compile_context → render_context` for **all** sources. ~57 LOC redundant.

### R2 — Duplicate Halstead implementation
`analyzer/visitors/halstead.py:65` `calculate_halstead_metrics(tree)` is the real,
AST-based implementation (used via `ast_metrics.py:82` → `worker.py:142`).
`analyzer/builders/calculator.py:103` `calculate_halstead_metrics(n1, n2, N1, N2)` has the
**same name** and **no callers** (nor `MetricsCalculator.halstead_metrics`).

### R3 — Dead `html` output path
`cli/commands/analysis.py:11-16` restricts `analyze --format` to `markdown|json`
(commit `7061f6d`), yet the HTML branch survives in:
`sources/pipeline.py:140`, `analyzer/engine.py:142`, and the
`summary_generator`/`reporting` HTML support. Unreachable.

### R4 — Name collisions that hide ownership

| Collision | Files |
| :--- | :--- |
| `parser` | `providers/parser.py` (GitParser) vs `builders/parser.py` (`parse_dependency_files`) |
| `analyzer` | `providers/analyzer.py` (GitAnalyzer) vs `analyzer/engine.py` (ProjectAnalyzer) |
| `report` / `reports` | `cli/commands/report.py` (helper) vs `reports.py` (command) |
| `providers` vs `sources` | `analyzer/providers/` (engine internals) vs `sources/` (source abstraction) |

### R5 — Payload computed but never rendered
`builders/ai_context_generator.py:6` renders only four sections
(`structure, metrics, dependencies, git`). Yet `sources/pipeline.py:60-76`
(`_ensure_defaults`) and the external mapping (`sources/external/qgis_analyzer.py`)
still populate `security`, `qgis_compliance`, `patterns`, `antipatterns`,
`recommendations` — dead payload in context-only mode (some survive only for
`PROJECT_SUMMARY`, which `context` does not emit).

### R6 — Duplicated `rich` fallback block
Identical `try: from rich... except ImportError: class Console/Table` stubs in
`cli/commands/compare.py:10-27` and `cli/commands/roadmap.py:8-25`. Extract a shared helper.

---

## 2. Dead code

| Item | Location | Evidence |
| :--- | :--- | :--- |
| `maintenance_group` click group | `cli/commands/maintenance.py:7` | 0 references |
| `graph_engine` alias | `analyzer/__init__.py:20` | 0 references |
| `ContextAggregator` facade + `warn_deprecated` | `builders/aggregator.py:99-110`, `deprecations.py` | 0 refs · `REMOVAL_VERSION="5.0.0"` already reached |
| Halstead (calculator) | `builders/calculator.py:103`, `:69` | 0 callers |
| `extra_data` parameter | `builders/calculator.py:202` | never read |
| `get_category` methods | `visitors/checker_base.py:28`, `visitors/optimization_checker.py:10` | unused |
| `SummaryGenerator` alias | `builders/summary_generator.py:77` | alive only via 1 test |
| Removed-command stubs | `cli/commands/deprecated.py` | deprecation cycle (retire in 5.1) |
| Orphan fixture `test_project/` | repo root (3 tracked files) | 0 references |
| Root scratch/cruft | `current_metrics.json` (empty), `full_analysis.md`, `report.md`, `test_strategy.py`, `audit_quality.py`, `check_docs.py`, `base.json`, `test_analysis.json`, `.ai-context/prompt_inicial.md`, `src/ai_context_core.egg-info/` | stale/history dumps |

> Non-findings: `analyzer/registry.py` is used (`visitors/ast_visitors.py:14`,
> `providers/worker.py:167`) but registers exactly **one** detector — over-engineered.
> `context/symbol_index.py:109 load_symbol_index` is used only by a test (public API).
> The `unused variable 'kwargs'` hits in `compare.py`/`roadmap.py` are **false positives**
> (rich fallback stubs).

---

## 3. Compatibility & metadata debt

- **`ast.Str` deprecation**: `visitors/sloc_helpers.py:27` uses
  `getattr(ast, "Str", ast.Constant)`, which emits `DeprecationWarning` (and `ast.Str` is
  removed in Python 3.14). Simplify to `ast.Constant`.
- **Legacy config**: `providers/config_loader.py` still reads `.ai-context/config.yaml`
  (deprecated path warning). Schedule removal.
- **Python target**: `requires-python >=3.9`; no `from __future__ import annotations` and no
  PEP-604 unions — currently compatible, but the target should be revisited.
- **Coverage hot spots** (`pytest --cov`): `cli/commands/compare.py` 18%, `roadmap.py` 18%,
  `report.py` 19%, `graph.py` 30%, `builders/git_tech.py` 39%, `providers/gis_utils.py` 48%,
  `builders/issues.py` 55%.
- **Packaging**: `pyproject.toml:4` description is stale ("Core logic for AI-driven
  development context management" vs. README "context compiler"); classifier
  `Development Status :: 4 - Beta` at 5.0.0; `[tool.uv.sources] ai-context-core = { workspace = true }`
  is a self-reference unusual for a published package.

---

## 4. Prioritized recommendations

**P0 — Collapse the render divergence (R1/R3).** Route `run_analysis` and `run_context`
through `compile_context → render_context` for every source; delete
`ProjectAnalyzer.analyze()`/`_generate_outputs()` and all HTML branches. One path → one
provenance/schema. ~90 LOC removed.

**P1 — Retire expired v4 residue.** Delete `ContextAggregator` + `deprecations.py` (window
elapsed), `graph_engine`, `maintenance_group`, the calculator Halstead, `extra_data`,
`get_category`, the `SummaryGenerator` alias; stop populating unrendered payload fields (R5).

**P2 — Repository hygiene.** Remove orphan `test_project/` and root cruft
(`base.json`, `test_analysis.json`, `current_metrics.json`, `full_analysis.md`, `report.md`,
`test_strategy.py`, `audit_quality.py`, `check_docs.py`, `.ai-context/`, `egg-info/`); move
historical reports to `docs/archive/`.

**P3 — Naming clarity.** Rename `analyzer/providers/` → `analyzer/engine/` (or fold into
`sources/builtin/`) to disambiguate from `sources/`; split `parser`/`report`; extract the
`rich` fallback.

**P4 — Robustness & quality.** Use `ast.Constant`; raise coverage on the low-coverage CLI
commands and `git_tech`/`gis_utils`/`issues`; update `pyproject` description/classifier.

---

## 5. Verdict

v5.0.0 has the right architecture (`sources → transform → render → verify`, 88% coverage),
but it still carries a **latent second pipeline (v4)** and several **expired
facades/aliases** that contradict the "context-only" contract. The remaining cleanup effort
concentrates on **P0 (single render path)** and **P1 (remove vencidas)**; everything else is
hygiene.
