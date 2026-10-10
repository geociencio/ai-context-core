# Implementation Plan: v5.1.0 — Context Alignment & Hardening

**Status**: PROPOSED — revised after `/ia-critic` (verdict FAILED); awaiting @architect re-approval to start P0
**Created**: 2026-10-10
**Revised**: 2026-10-10 (folded ia-critic corrections 1–10; see §9)
**Owner**: @architect (+ @qa_engineer for verification, @auditor for scope discipline)
**Target repo**: `~/qgispluginsdev/ai-context-core` (PyPI `ai-context-core`)
**Baseline**: v5.0.1 (current) · 182 tests passing (`uv run pytest -q`)
**Relates to**: `docs/adr/0008-context-only-contract.md`,
`docs/reviews/audit_architecture_redundancies_v500.md`,
`docs/plans/implementation_plan_ai_context_core_context_only_v5.md`

---

## 0. Context

The v5.0.0 context-only contract is implemented and v5.0.1 is released (GitHub +
PyPI). A post-release evaluation of the codebase, its generated artifacts and its
agentic configuration (2026-10-10) found a consistent pattern: **the machine is
coherent, but the surfaces that describe and wire it have drifted.** Specifically:

- the project's own `AGENTS.md` still describes the pre-v5 identity and references
  a **removed** command (`ai-ctx audit`) and a **deleted** module
  (`visitors/i18n.py`);
- `forge.toml` declares `analyzer_command` that **no tool consumes**;
- the bundled `templates/workflows/*.md` (emitted by `ai-ctx init`) are the old
  v4 workflows;
- the flagship artifact (`AI_CONTEXT.md`) is **not token-efficient by default**
  (most of its tokens are a Mermaid diagram dominated by styling lines);
- the external single-source path (`--source external`) is **unit-tested but not
  exercised against a real `qgis-plugin-analyzer` payload** in this environment;
- the analyzer's own unused-import detector misreports intentional re-export
  imports, and several active docs still describe removed v3 domains.

This plan closes those gaps. It is **alignment/hardening**, not new features, and
therefore respects the ADR-0008 feature freeze (no new analysis capabilities).

### Non-goals (unchanged from ADR-0008)

QGIS compliance, i18n AST audit, security scanning, quality gates, lint/format and
scaffolding remain owned by `qgis-plugin-analyzer`, `ruff` and `agentic-forge`.

---

## 1. Evidence (evaluation 2026-10-10; locations verified against the tree)

| # | Finding | Location (verified) | Impact |
| :-: | :--- | :--- | :--- |
| E1 | Identity still promises "deep AST analysis … QGIS plugin hygiene" | `AGENTS.md:3` | Misleads agents about the v5 contract |
| E2 | Self-analysis lists removed command `ai-ctx audit --threshold 70` | `AGENTS.md:85` (stub: `cli/commands/deprecated.py`) | Broken command reference |
| E3 | i18n rule references deleted `visitors/i18n.py`; visitor list still names i18n/patterns/security | `AGENTS.md:130` and `AGENTS.md:102` | Phantom path + stale model |
| E4 | `analyzer_command` declared but unused by any framework tool | `forge.toml:16` (0 refs in `.agent/`) | Dead config; no automated self-analysis |
| E5 | Only two framework files name `ai-ctx` | `.agent/scaffold/qgis/workflows/release-plugin.md:71`, `.agent/skills/commit-standards/SKILL.md:19` | Adoption is manual/implicit |
| E6 | Bundled templates are v4 (`ai-ctx analyze`, `task.md`, `end-session`, `unittest`) | `src/ai_context_core/templates/workflows/*.md`, copied by `cli/commands/init.py:32-36` | `ai-ctx init` scaffolds obsolete workflows |
| E7 | `[context.budget]` commented out → default render unbounded | `src/ai_context_core/config/defaults.toml:15-19`; `context_manifest.json` `"budget": null` | "Token-efficient" claim unenforced |
| E8 | `dependencies` = 2,047 / 2,680 tokens (76%); 87 `classDef`/`class … module;` lines (~37% of the Mermaid diagram) | `context_manifest.json`; `builders/reporting.py:78-80` | Marginal-value styling dominates the artifact |
| E9 | `_ensure_defaults` seeds retired-domain keys | `sources/pipeline.py:60` (keys at `:68,69,72,73`) | Payload advertises retired domains (builtin) |
| E10 | Default dev env lacks `analysis_results/` / `qgis-plugin-analyzer` → `auto` resolves to builtin in practice. **The external path is already covered** by `tests/test_sources.py` (mapping, provenance, `auto` selection, CLI) | `sources/base.py:108-112`; `tests/test_sources.py:94-274` | Only a *real-schema* fixture is missing, not coverage |
| E11 | The analyzer's own UNUSED IMPORTS detector flags `algorithms.py:5` and `worker.py:132`, but both are **intentional** (`# noqa: F401` re-export / detector-registration side-effects). **`cycle_detector.py` is live** | `dependencies.py:7,103,118`; `tests/test_dependencies_extended.py:10`; `algorithms.py:5`; `worker.py:132` | Detector false positive, not dead code |
| E12 | `docs/ARCHITECTURE.md` describes v3.2.0 (`audit`, `security`, Jinja2/HTML) | `docs/ARCHITECTURE.md:17,38,42,71` | Stale architecture doc |
| E13 | `docs/CONFIGURATION.md` documents retired domains | `docs/CONFIGURATION.md:84-98` (`[security_patterns]`), `:124-148` (`[patterns.i18n]`) | Active doc documents removed features |

---

## 2. Scope, ownership & guardrails

| Surface | Owner | Changeable in this repo? |
| :--- | :--- | :--- |
| `AGENTS.md`, `forge.toml`, `docs/`, `src/`, `tests/` | ai-context-core | Yes |
| `.agent/` submodule (workflows, skills, `forge.py` tooling) | `agentic-forge` | No — cross-repo (like F5) |
| `.agent-state/` (overlay skills, memory, task) | ai-context-core | Yes |
| `qgis-plugin-analyzer` output schema | `qgis-plugin-analyzer` | No — consume only |

**Guardrails**
- No new analysis capability is introduced (ADR-0008 freeze). Every item is either
  documentation, wiring, token shaping, a test, or removal of misreported dead code.
- No behavior change that breaks existing artifacts without a changelog entry and a
  regenerated golden fixture.
- `project_context.json` remains backward compatible; removed keys must be **absent**
  rather than repurposed.
- Any config change requires `--no-cache` in verification (Lesson: config does not
  invalidate the module cache).

---

## 3. Workstreams

### WS-1 — Agentic documentation alignment (in-repo)
**Goal**: every agent-facing surface describes v5.0.1 accurately.

- `AGENTS.md:3` — reword the identity: context **compiler** (`source → transform →
  render → verify`); note that QGIS/i18n/security hygiene is owned by
  `qgis-plugin-analyzer`.
- `AGENTS.md:85` — replace the self-analysis block: `analyze`, `context`, `stats`,
  `verify`, `health` (drop `audit`).
- `AGENTS.md:102` — fix the visitor list (no i18n/patterns/security).
- `AGENTS.md:130` — remove the `visitors/i18n.py` / i18n-heuristics rule.
- `.agent-state/skills/project-context/SKILL.md` and `domain-logic/SKILL.md` — audit
  for the same v4 residue; align with the context-only pipeline.

**Exit**: `rg "ai-ctx audit|visitors/i18n\.py" AGENTS.md .agent-state/skills` → 0
hits. `.agent-state/history/` and historical narrative sections (e.g.
`next_steps.md` "Completed" entries) legitimately record past states and are
excluded. A new agent reading `AGENTS.md` learns only real, existing commands.

### WS-2 — Workflow wiring (split: in-repo doc + cross-repo framework)
**Goal**: self-analysis is actually invoked, not implied.

- **In-repo (now)**: make `AGENTS.md` the canonical self-analysis reference and
  document that `forge.toml [project].analyzer_command` (`forge.toml:16`) is the
  intended hook.
- **Cross-repo (proposal → `agentic-forge`)**: consume `[project].analyzer_command`
  in `/start-session` (§2 Quick Quality Scan) and `/audit-package` (§1 Full
  Analysis) so the placeholder becomes the real command. Same treatment as the
  deferred F5.

**Q1 resolved**: propose the framework change and **keep** the key.

### WS-3 — Token efficiency of `AI_CONTEXT.md`
**Goal**: the default artifact is compact and the budget is meaningful.

- `builders/reporting.py:78-80` — make the Mermaid `classDef`/`class … module;`
  styling block **optional** via a typed flag (e.g. `[context].mermaid_style = false`)
  and drop it by default; keep the edges. Record measured before/after.
- `src/ai_context_core/config/defaults.toml:15-19` — set default budget: `max_tokens = 8000` and
  `[context.budget.sections] dependencies = 2500` (Q3 resolved).
- `context/budget.py` / `context/manifest.py` — no logic change expected; assert
  `total == header + sum(sections)` still holds.
- **New test**: the golden tests call `render_context(result, proj, {})` with an
  **empty** config (`tests/test_golden_reports.py:27-28`), so they do **not**
  exercise the new defaults — add a dedicated test that loads
  `config/defaults.toml` and asserts the budget is applied.
- Regenerate goldens deliberately and review the diff.

**Measured** (this repo, `ai-ctx context --no-cache`): total **2680 → 2056** tokens
(-23%), `dependencies` **2047 → 1423** (-30%); manifest now reports `budget: 8000`
and `truncated: false`. Golden diff = the 3 removed `classDef`/`class … module;`
lines only.

**Exit** (hard): default `AI_CONTEXT.md` token count drops (measured, recorded in
this plan); `context --check` green after `--no-cache`; `--max-tokens N` never
exceeds `N`; new defaults test passes.

### WS-4 — Contract fidelity: retired domains (builtin **and** external)
**Goal**: the payload no longer advertises capabilities we do not own.

- `sources/pipeline.py:68,69,72,73` — remove `security`, `qgis_compliance`,
  `patterns`, `antipatterns` from `_ensure_defaults`.
- `sources/external/qgis_analyzer.py:114-118` — stop emitting the same four keys
  (the guardrail "removed keys must be absent" must hold for external too).
- Safe because no consumer subscripts them directly: `builders/issues.py:11` uses
  `.get("security", [])` with a default. Confirm during implementation.
- Update `tests/test_sources.py` assertions and any payload snapshots.

**Exit**: a builtin- **and** external-sourced `project_context.json` contain none of
the four keys; tests pass.

**Done (P2)**: keys removed from `_ensure_defaults` (`sources/pipeline.py`) and
`map_project_context` (`sources/external/qgis_analyzer.py`). Two regression tests
added (`test_map_project_context_drops_retired_domains`,
`test_builtin_payload_has_no_retired_domains`). Regenerated `project_context.json`
has no top-level `security`/`qgis_compliance`/`patterns`/`antipatterns`
(remaining `antipatterns.py` hits are git-churn history for deleted files).

### WS-5 — External source fixture (FOLDED into WS-4)
**Status**: folded. The external adapter was already covered by
`tests/test_sources.py` (mapping, provenance, `auto` selection, CLI) — confirmed by
`/ia-critic`. Rather than duplicate a fixture, WS-4 strengthened the same suite
with the retired-domain assertions. No separate fixture file is added (avoids
redundancy).

**Exit**: met via WS-4's tests; `tests/test_sources.py` green.

### WS-6 — Unused-import false positive (NOT dead-code deletion)
**Goal**: stop the analyzer from misreporting intentional re-exports.

- **Do not delete `analyzer/builders/cycle_detector.py`** — it is live via
  `dependencies.py:7,103,118`.
- Fix the real issue: the unused-import detector should honor a trailing
  `# noqa: F401` (and/or treat re-export/registration imports as used) so
  `algorithms.py:5` and `worker.py:132` are no longer flagged.
- **Mechanism note**: AST does not retain comments; honoring `# noqa: F401`
  requires tokenize-based line mapping — the **same** helper as the `# no-i18n`
  opt-out (`AGENT_LESSONS.md`). Reuse it, single implementation.
- Add a regression test for the `# noqa: F401` opt-out.
- Re-scan for genuinely dead modules; if none, drop the "dead code" framing.

**Exit**: `uv run ai-ctx analyze --no-cache --path .` reports zero unused imports;
`ruff` clean; `tests/test_self_score.py` CC budget (≤25) respected — **do not merge
modules** (Lesson: the `X.py` + `X_rules.py` split is intentional).

**Done (P3)**: new `visitors/noqa.py` (`find_noqa_lines`, tokenize-based); the
registered `unused_imports` detector now receives `content` (`worker.py`) and skips
statements with a `# noqa` / `# noqa: F401` directive. `imports_visitor.py` was kept
under the CC 25 budget by extracting `noqa.py` + `_is_unused` (self-score gate
passed at CC 29 → refactored). Regression tests: `tests/test_unused_imports_noqa.py`.
`ai-ctx analyze --no-cache` no longer emits an UNUSED IMPORTS section.

### WS-7 — Documentation & template modernization
**Goal**: docs and scaffolds match v5.

- Rewrite `docs/ARCHITECTURE.md` for the v5 pipeline; drop v3.2.0 references
  (`:17,38,42,71`).
- Edit `docs/CONFIGURATION.md`: remove `[security_patterns]` (`:84-98`) and
  `[patterns.i18n]` (`:124-148`).
- Replace `src/ai_context_core/templates/workflows/*.md` per WS-8.

**Exit**: `rg "v3.2.0|security_patterns|patterns\.i18n" docs/ARCHITECTURE.md
docs/CONFIGURATION.md` → 0 hits.

**Done (P3)**: `docs/ARCHITECTURE.md` rewritten for the v5 pipeline (sources →
context → render → verify); `docs/CONFIGURATION.md` rewritten — removed
`[security_patterns]` and `[patterns.i18n]`, added a `[context]` section
(`sections`/`mermaid_style`/`budget`) and a `--no-cache`-after-config note.

### WS-8 — `ai-ctx init` behavior (Q2 resolved: remove templates, defer to `.agent`)
**Goal**: removing the stale templates must not silently scaffold nothing.

- Today `init.py:32-36` globs `templates/workflows/*.md` and copies them into the
  target's `.agent/workflows/`. Removing the files makes it copy **zero**.
- Define the replacement: (a) stop shipping workflows and print a clear notice that
  workflows are provided by `agentic-forge` (mount `.agent/`), keeping
  `.ai-context/` + `initial_prompt.md`; or (b) embed a minimal, framework-agnostic
  scaffold. **Prefer (a)** (framework is the single source).
- Update `init.py` and add a test asserting the notice / no stale files
  (`tests/test_cli.py:7` only asserts exit code today).

**Exit**: `ai-ctx init` on a scratch dir produces no v4 workflows and prints a
framework pointer; test covers it.

**Done (P3)**: removed `src/ai_context_core/templates/workflows/*.md`; `init.py` no
longer creates `.agent/workflows/`, keeps `.ai-context/` + `prompt_inicial.md`, and
prints the agentic-forge pointer. Test: `test_init_defers_workflows_to_framework`.

---

## 4. Phased execution

### P0 — Documentation & config alignment (WS-1, WS-2 in-repo)
- Edit `AGENTS.md` (`:3`, `:85`, `:102`, `:130`), overlay skills; document the
  `analyzer_command` hook.
- **Exit**: no phantom commands/paths in agent surfaces; no behavior change.

### P1 — Token efficiency (WS-3)
- Optional Mermaid styling + default budget (8000 / dependencies 2500); new
  defaults test; regenerate goldens.
- **Exit**: measured token drop recorded; `context --check` green.

### P2 — Contract fidelity (WS-4) + external fixture (WS-5)
- Prune retired keys from builtin `_ensure_defaults` **and** external mapping; add
  the realistic fixture.
- **Exit**: payload free of retired domains (builtin + external); tests pass.

### P3 — Detector fix & docs/templates (WS-6, WS-7, WS-8)
- Honor `# noqa: F401`; rewrite `ARCHITECTURE.md`; edit `CONFIGURATION.md`; rework
  `init` behavior + test.
- **Exit**: analyze reports zero unused imports; docs v5-consistent; `init` notice
  covered.

### P4 — Release v5.1.0
- Version sync (`pyproject`, `__init__`, `uv.lock`), CHANGELOG, release notes,
  `scripts/sync_metrics.py`, golden refresh, build + `twine check`, tag + GitHub
  release; PyPI upload handed to the maintainer.
- Commit the pytest-regenerated root artifacts (`AI_CONTEXT.md`,
  `PROJECT_SUMMARY.md`, `project_context.json`, `context_manifest.json`) as a
  separate `chore(docs)` commit (Lesson: pytest dirties the tree).

---

## 5. Risks & mitigations

| Risk | Mitigation |
| :--- | :--- |
| Optional Mermaid styling / budget breaks golden tests | Regenerate goldens deliberately; add a dedicated defaults test |
| Default budget truncates legitimate large projects | Keep configurable; document override; assert `--max-tokens` only |
| Removing `_ensure_defaults` / external keys breaks consumers | Land with WS-5 fixture; verify `.get` defaults; update snapshots |
| Removing templates makes `init` copy nothing | WS-8 defines the notice + test |
| "Fixing" `# noqa` imports touches detection semantics | Regression test; keep scope to the opt-out only |
| Framework workflow change requires submodule edits | Cross-repo (agentic-forge); in-repo part limited to docs |
| Scope creep toward re-adding analysis | @auditor gate: reject any new analysis capability |

---

## 6. Verification

- Per phase: `uv run ruff check . && uv run ruff format --check .` and
  `uv run pytest -q` (baseline **182 passed**; do not regress).
- After any config edit: add `--no-cache` (e.g. `ai-ctx analyze --no-cache`).
- Token claim: before/after `context_manifest.json` totals recorded in this plan
  (hard exit for P1).
- Contract: `project_context.json` (builtin **and** external) contains no
  `security`/`qgis_compliance`/`patterns`/`antipatterns` keys.
- Unused imports: `uv run ai-ctx analyze --no-cache --path .` → zero findings.
- Docs (scoped to **active** docs, not episodic logs):
  `rg "ai-ctx audit|visitors/i18n\.py|v3\.2\.0|security_patterns|patterns\.i18n"
  AGENTS.md docs/ARCHITECTURE.md docs/CONFIGURATION.md README.md`
  → 0 hits. Do **not** grep recursive `docs/` (history logs legitimately reference
  old states).
- `ai-ctx init` in a temp dir: no v4 workflows; framework notice printed.
- `ai-ctx health` stays fresh; `python .agent/tools/forge.py metrics validate`
  reports only the known framework-scaffold false positives.

---

## 7. Open questions

All resolved by user: Q1 (propose framework change, keep key), Q2 (remove templates,
defer to `.agent`), Q3 (8000 + `dependencies=2500`), Q4 (v5.1.0). See §9.

Residual implementation choice: WS-8 option (a) notice vs (b) minimal scaffold —
recommendation is (a).

---

## 8. Approval

Per the @architect constraint, **no code will be written or executed until the USER
re-approves this revised plan.** Recommended next action: confirm §9 corrections,
then execute P0 → P4.

---

## 9. ia-critic response (verdict FAILED → corrections folded)

The `/ia-critic` audit (`2026-10-10`, @auditor) returned **FAILED** with 10 required
corrections; all are now applied:

1. Evidence locations corrected (E1 `AGENTS.md:3`, E4 `forge.toml:16`, E5 full
   `.agent/scaffold/qgis/workflows/...` path, E7 `config/defaults.toml:15-19`, and
   `AGENTS.md:104` → `:102`).
2. **E10/WS-5 rewritten**: the external path is already unit-tested
   (`tests/test_sources.py`); WS-5 is re-scoped to a realistic fixture and the
   uncovered-coverage claim removed.
3. **E11/WS-6 rewritten**: `cycle_detector.py` is live; the flagged imports are
   intentional `# noqa: F401`; WS-6 now fixes the detector instead of deleting code.
4. Section-6 grep scoped to active docs (history logs excluded).
5. WS-6 exit contradiction resolved (honor `# noqa`; don't imply removal).
6. WS-8 added: `ai-ctx init` behavior defined for the template removal + test.
7. WS-7 expanded to a definite `docs/CONFIGURATION.md` edit (E13).
8. WS-4 reconciled with the external mapping (`qgis_analyzer.py:114-118`).
9. Baseline corrected to 182; E8 wording fixed; token before/after made a hard exit.
10. `--no-cache` added to verification; P4 adds a separate `chore(docs)` commit for
    regenerated artifacts.

Observations adopted: dedicated defaults/budget test; `_ensure_defaults` removal
justified by `.get` defaults; preferred minimal `init` behavior.
