# Agentic Forge Audit — `.agent` v1.2.0

- **Date**: 2026-10-19
- **Framework**: `agentic-forge` v1.2.0 (`2de22cf`, git submodule at `.agent/`)
- **Project overlay**: `.agent-state/`
- **Scope**: framework skills, workflows, tooling, domain pack, project overlays, memory and metrics
- **Method**: static inspection plus execution of every `forge.py` subcommand
- **Nature**: read-only audit. No framework or project file was modified.

---

## 1. Executive summary

Agentic Forge has a clear and pragmatic design: framework content is reusable under
`.agent/`, project state is isolated under `.agent-state/`, and a single CLI
(`forge.py`) exposes validation, graph, conflict, metrics, memory and lesson tooling.
The submodule is clean, tagged `v1.2.0`, and all 14 workflows carry valid frontmatter.

The audit found **three high-severity defects that make quality gates unreliable**:

1. **`forge.py validate --graph` never fails on broken references** unless `--validate`
   or `--json` is passed, although the workflow claims it exits 1.
2. **`forge.py metrics validate` is permanently red** because it compares the QGIS
   domain pack and the generic `coding-standards` skill against this project's ground
   truth; `/close-session` treats that check as critical.
3. **`forge.py memory prune` cannot parse `AGENT_LESSONS.md`**, exits 0 on the error,
   and deletes `next_steps` snapshots without a dry-run default.

There is also significant **SSoT drift** between the root `AGENTS.md`,
`QUICK_REFERENCE.md` and the actual workflow frontmatter, and incomplete
genericization in `forge_metrics.py` and `lesson_extractor.py` (QGIS/SecInterp
constants survive in the "generic" core).

**Verdict**: the conceptual model is sound, but the tooling cannot currently enforce
the standards it documents. Fixing the gates (P0) is a prerequisite for trusting the
framework's metrics and memory.

---

## 2. Composition

| Component | Content |
| :--- | :--- |
| Framework | 9 core skills, 14 workflows, 5 Python tools (1,855 LOC) |
| Domain pack | `scaffold/qgis/`: 3 skills, 3 workflows, 1 resource |
| Project overlay | 6 skills under `.agent-state/skills/` |
| Project state | `next_steps.md`, `task.md`, memory (lessons, metrics, policy), history |
| Roles | `architect`, `qa_engineer`, `auditor` (registered in `opencode.json`) |
| Configuration | `forge.toml` (`framework`, `state`, `max_cc=25`, `module_size_limit=400`) |

The framework is **runtime-agnostic** (it works with any agent that reads
`AGENTS.md` + `SKILL.md`) but **Python-specific** in its tooling.

---

## 3. Verification results

Commands were run from the repository root.

| Command | Result |
| :--- | :--- |
| `python .agent/tools/forge.py validate` | ✅ 15 skills, 14 workflows, exit 0 |
| `python .agent/tools/forge.py validate --graph` | ⚠️ 0 broken refs, 6 "unreferenced" skills, **exit 0** |
| `python .agent/tools/forge.py validate --conflicts` | ✅ No conflicts, exit 0 |
| `python .agent/tools/forge.py metrics validate` | ❌ 5 inconsistencies, **exit 1** |
| `python .agent/tools/forge.py memory prune` | ⚠️ "Could not find YAML block", **exit 0** |
| `python .agent/tools/forge.py lesson propose` | No signals in `HEAD~1`, exit 0 |
| Tests for `.agent/tools` | ❌ None (1,855 LOC untested) |
| `git -C .agent describe` | `v1.2.0`, working tree clean |

---

## 4. High-severity findings

### A1. `validate --graph` does not fail on broken references

`validate_agent_system.py` implements `graph_main()`. It only calls `sys.exit(1)` when
`--validate` or `--json` is present:

```python
validate_only = "--validate" in sys.argv
...
if validate_only:
    sys.exit(1 if broken else 0)
```

`forge.py validate --graph` forwards only `--graph`, so the command prints the graph
and returns 0 even when `broken` is non-empty. The documented invocation in
`workflows/verify-standards.md`, `workflows/index.md` and `QUICK_REFERENCE.md` is
`forge.py validate --graph`, and the workflow explicitly promises:

> `--graph` exits with code 1 if any workflow references a missing skill or script.

**Impact**: the reference-integrity gate cannot block anything.

**Recommendation**: exit 1 whenever `broken` is non-empty, regardless of the flags
(keep `--json` for machine output), and add a regression test that creates a workflow
with a missing skill and asserts exit code 1.

### A2. `metrics validate` is permanently red and close-session is blocked

`forge.py metrics validate` returns **exit 1** with five violations:

- `scaffold/qgis/workflows/release-plugin.md`: 763 tests and CC 10 compared with the
  project ground truth (196 tests, CC ≤ 25).
- `.agent/skills/coding-standards/SKILL.md:54`: "Keep cyclomatic complexity below 10"
  compared with `max_cc = 25` in `forge.toml`.

Two independent problems:

1. `should_skip_file()` excludes `history/` and `architecture/`, but **not
   `scaffold/`**, so the QGIS domain pack and generic skills are validated against
   this project's metrics.
2. The generic skill hardcodes CC < 10 while the project explicitly sets `max_cc = 25`
   and the project self-score uses 25. There is no single source of truth.

`workflows/close-session.md` marks this check as **CRITICAL** ("Fix any reported
inconsistencies before proceeding"), so the session-closing flow either blocks or
requires ignoring a critical gate. The project's own `AGENT_LESSONS.md` already
documents these false positives (2026-10-08), but the tool was not fixed.

**Recommendation**: exclude `scaffold/` from project-truth checks; make
`coding-standards` refer to the project limit (`[project].max_cc`) instead of
hardcoding 10; or split "framework metrics" from "project metrics".

### A3. `memory prune` cannot parse the lessons file and exits 0 on error

`memory_prune.py` expects a fenced YAML block:

```python
yaml_match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
if not yaml_match:
    print("Error: Could not find YAML block in AGENT_LESSONS.md")
    return 0
```

`AGENT_LESSONS.md` uses Markdown bullets (`- date: ...`). The command prints an error,
prunes nothing and exits 0. Additional defects:

- `import yaml` (PyYAML) is undeclared; a clean environment fails at import time.
- `prune_next_steps_snapshots()` deletes files older than 90 days with no dry-run, and
  `/close-session` invokes it.
- Because pruning never works, stale lessons persist. Concrete example: the lesson
  "Config changes do not invalidate the module cache" contradicts the current
  `engine.py` / `fs_cache.py` implementation, which includes the configuration
  fingerprint in the cache key.

**Recommendation**: parse the Markdown bullets (or migrate the file to a real YAML
block), make `--dry-run` the default and require `--apply` to delete, exit non-zero on
parse errors, and declare PyYAML (or drop the YAML path entirely).

---

## 5. Medium-severity findings

| # | Finding | Evidence |
| :--- | :--- | :--- |
| B1 | **Root `AGENTS.md` is out of sync**: 13 workflow commands vs 14 in the framework (`/i18n-maintenance` missing); 5 overlay skills listed vs 6 on disk (`release-ai-context-core` only mentioned in prose). | `AGENTS.md` vs `.agent/workflows/`, `.agent-state/skills/` |
| B2 | **`QUICK_REFERENCE.md` workflow→skills table is stale** vs actual frontmatter: `/start-session` declares 2 skills, uses 3; `/close-session` declares 2, uses 5; `/verify-standards` declares 1, uses 3. | `forge.py validate --graph` output |
| B3 | **`verify-standards.md` demands a structure the framework does not follow**: "When to use / Degree of Freedom / Workflow / Instructions / Quality Checklist". Only 5/9 core skills have it; `documentation-standards`, `i18n-standards`, `agentic-memory` and `changelog-generator` do not. `--conflicts` also only checks duplicate names/descriptions, not "skills that share the same trigger" as the workflow claims. | `.agent/skills/*/SKILL.md`, `validate_agent_system.py` |
| B4 | **`forge_metrics.py` is not generic** (705 LOC): hardcoded `Security (Bandit)`, i18n AST gate and `qgis_analyzer` ground truth; `STALE_MAPPINGS` uses reference-project values (535→620, 40.8→52.3, CC 15→10); `ARCHAIC_MARKERS` v3.x. `--fix` can write 10 where the project expects 25. | `.agent/tools/forge_metrics.py` |
| B5 | **`lesson_extractor.py` retains QGIS/project assumptions**: `self.tr(...)`, `# no-i18n`, `qgis-analyzer`, `core/`, `gui/`, `exporters/` categories, 535/572/620 metrics. It proposes `scripts/sync_metrics.py --validate`, but `sync_metrics.py` has no argument parsing. | `.agent/tools/lesson_extractor.py`, `scripts/sync_metrics.py` |
| B6 | **Tooling requires Python 3.11+ while the project declares 3.9**: `forge_paths.py` imports `tomllib` without fallback; `sync_metrics.py` uses `Path \| None` (3.10+). On 3.9/3.10 `forge.py` fails before validating. | `.agent/tools/forge_paths.py`, `scripts/sync_metrics.py` |
| B7 | **`memory_policy.md` points to wrong paths**: `.agent/memory/...` instead of `.agent-state/memory/...`; it also describes a "YAML-structured" format the real file does not use. | `.agent-state/memory/memory_policy.md` |
| B8 | **Stale semantic memory**: lessons reference removed domains (i18n opt-out, `find_no_i18n_lines`) and an outdated cache behavior; the broken pruning prevents consolidation. | `.agent-state/memory/AGENT_LESSONS.md` |
| B9 | **No tests for the tooling**: 1,855 LOC, including a 705-line module that exceeds the project's `module_size_limit = 400`. `metrics validate` only scans `.md`/`.json`, so it cannot catch this. | `.agent/tools/*.py` |
| B10 | **`README.md` claims a `pre-push` hook** enforcing complexity and style. Only a `pre-commit` hook with Ruff exists; there is no pre-push hook and no complexity check. | `.agent/README.md:17`, `.pre-commit-config.yaml`, `.git/hooks/` |

---

## 6. Strengths

- **Clear framework/state separation**: `.agent` is reusable; `.agent-state` is owned by
  the project.
- **Robust path resolution**: `forge_paths.py` discovers `forge.toml` by walking up, so
  the tooling survives moving `.agent/`.
- **14 workflows with consistent frontmatter** (`description`, `agent`, `skills`,
  `validation`, `stop_conditions`).
- **9 core skills + 6 overlay skills** pass frontmatter validation; the workflow graph
  reports zero broken references.
- **Single CLI** for validate/graph/conflicts/metrics/memory/lesson.
- **Clean submodule**: tagged `v1.2.0`, clean working tree, `__pycache__` ignored.
- **QGIS domain pack is correctly separated** and its 3 skills are tracked.
- **Ground truth is synchronized**: 196 tests, quality 95.3, CC ≤ 25.

---

## 7. Prioritized action plan

| Priority | Action |
| :--- | :--- |
| **P0** | Make `validate --graph` exit 1 on broken references by default (or change every documented invocation to `--graph --validate`). |
| **P0** | Exclude `scaffold/` from project-truth metrics and resolve the CC 10 vs 25 conflict with a single source of truth. |
| **P0** | Fix `memory prune`: parse Markdown bullets, default to dry-run, exit non-zero on error, and declare PyYAML. |
| **P1** | Sync root `AGENTS.md` (add `/i18n-maintenance` and `release-ai-context-core`). |
| **P1** | Regenerate or update `QUICK_REFERENCE.md` from `--graph`. |
| **P1** | Align `verify-standards.md` with the real skill structure, or complete the missing skills. |
| **P1** | Genericize `forge_metrics.py` and `lesson_extractor.py`; remove or parameterize `STALE_MAPPINGS`. |
| **P1** | Add tests for `.agent/tools` (frontmatter, broken graph, metric exclusions, prune parser) and a framework CI job. |
| **P2** | Declare the tooling Python floor (3.11+) and its dependencies, or add a `tomli` fallback. |
| **P2** | Fix `memory_policy.md` paths, clean stale lessons, and correct the `pre-push` claim in the README. |

---

## 8. Cross-cutting observation

The repository and the framework share the same failure mode: **gates that do not
gate, and documentation that promises more than the code enforces**.

- Repository CI runs a removed `audit` command (exit 0) and never runs Ruff.
- `.agent` `validate --graph` returns 0 on broken references, `memory prune` cannot
  parse its input, and `metrics validate` is red for false positives.
- Both projects maintain README/AGENTS/QUICK_REFERENCE tables by hand, and they drift
  from the code.

The repository has 196 tests and 89% coverage; the framework tooling has **zero tests**.
That is the highest structural risk in the agentic system.

---

*Independent audit of `agentic-forge` v1.2.0 as mounted in `ai-context-core`. No file
was changed.*
