# Repository Audit — ai-context-core v5.1.0

- **Date**: 2026-10-19
- **Version audited**: 5.1.0 (`d05afe7`, branch `main`)
- **Scope**: source, tests, configuration, generated artifacts, documentation, packaging and CI
- **Method**: static inspection plus reproducible execution of the test suite, linters, lockfile,
  CLI and a controlled determinism experiment on a disposable copy
- **Nature**: read-only audit. No source file was modified.

---

## 1. Executive summary

`ai-context-core` is a **context compiler** (`source → transform → render → verify`) with a
clean layered architecture and a strong test suite: **196 tests passing**, **89% coverage** and a
clean **Ruff** run. The core pipeline (`sources/` → `context/` → `analyzer/` builders) is well
separated and the source-provider protocol is a sound design.

The audit found **four high-severity issues that affect the product's core promises**, plus a
set of documentation and packaging defects:

1. **Generated artifacts are not reproducible** across runs (module ordering follows parallel
   completion order).
2. **`verify` reports "fresh" for stale context** when the staleness source is configuration,
   an embedded markdown document, or `symbols.json`.
3. **Python 3.9/3.10 silently lose `defaults.toml`** because `tomli` is not a declared dependency
   (and CI does not catch it).
4. **The CI quality gate is a no-op**: it invokes the removed `audit` command, which exits 0,
   and Ruff is never executed in CI.

**Verdict**: the architecture is sound, but the "versioned, verifiable, deterministic" contract
is not fully enforced by the implementation or by CI. The P0 fixes below are prerequisites for a
credible 5.1.x patch release.

---

## 2. Architecture overview

| Layer | Contents | Assessment |
| :--- | :--- | :--- |
| `sources/` | `AnalysisProvider` protocol, `builtin` engine source, `external` qgis-analyzer adapter, hybrid pipeline | Well isolated |
| `model/` | `AnalysisResult` + `Provenance` | Clean, but provenance reaches only JSON artifacts |
| `context/` | `budget`, `manifest`, `verify`, `health`, `symbol_index` | Solid; `verify` has blind spots |
| `analyzer/` | engine → providers → visitors/builders → reporting | Correct separation; v4 residue remains |
| `cli/` | Click commands, thin dispatch | Mostly correct; inspection commands bypass `--source` |

Size: **105 Python modules, 6,636 LOC** in `src/`; **41 test files, 2,823 LOC** in `tests/`.

---

## 3. Verification results

All commands were executed from the repository root. The sandbox had a read-only `~/.cache/uv`,
so `UV_CACHE_DIR=/tmp/uv-cache` was used for `uv run`.

| Check | Result |
| :--- | :--- |
| `uv run pytest -q` | ✅ 196 passed, 2 warnings, 1.45 s |
| `uv run pytest -q --cov=ai_context_core --cov-report=term-missing` | ✅ 89% (2,854 statements, 305 missed) |
| `uv run ruff check .` | ✅ All checks passed |
| `uv run ruff format --check .` | ✅ 147 files already formatted |
| `uv lock --check` / `uv sync --dry-run` | ✅ Lockfile consistent (77 packages) |
| `uv run ai-ctx stats` | 105 modules, 4,075 SLOC, 6,636 physical lines, score 95.3, MI 55.2 |
| `uv run ai-ctx verify` | ✅ "Context is fresh." |
| `uv run ai-ctx health` | 2,009 / 8,000 tokens, 440 definitions, 285 references |
| Wheel `dist/ai_context_core-5.1.0-py3-none-any.whl` | ✅ Includes `config/defaults.toml` and `templates/`; `Requires-Dist: click, rich` |

The two pytest warnings come from the deprecated `.ai-context/config.yaml` fallback
(`config_loader.py:93`).

---

## 4. High-severity findings

### H1. Generated artifacts are not deterministic

**Evidence.** Three consecutive `ai-ctx context --no-cache` runs on an identical copy of the
project produced three different `AI_CONTEXT.md` files:

```
run1 7f49560ec920a85d6b8d126b0fdcbb0323969ba88de101c47d638ef9d28012af
run2 517e63207938148d55411679f473f1aa4ae6b9b0b95bb1145d048c1438b8fbdf
run3 aa1032d5589b3b86f2c52e054f6c620392e5257c639142f816c78e6068e0f8c1
```

The diff reorders coupling (CBO) blocks, optimization recommendations and module entries. A warm
cache run produces yet another hash.

**Root cause.** `AnalysisWorker.run_parallel` appends batch results in `as_completed` order
(`src/ai_context_core/analyzer/providers/worker.py#L89-L103`) and `ResultsAggregator` returns
`"modules": m_data` unsorted (`src/ai_context_core/analyzer/builders/aggregator.py#L89`). With
`PARALLEL_MIN_FILES = 5` and 105 modules, the process pool is always used.

**Impact.** Contradicts the documented "deterministic truncation" (`README.md:42`), makes committed
artifacts churn on every run and changes `context_manifest.json` token deltas.

**Recommendation.** Sort results by path before returning from `run_parallel` (or in the
aggregator), and add a regression test that renders a >5-module fixture twice and compares bytes.

### H2. `verify` can certify stale context as fresh

**Evidence.** `verify` tracks only three artifacts (`src/ai_context_core/context/verify.py#L22`)
and hashes only `.py` files (`#L48-L71`). Three controlled experiments returned false positives:

| Change | `verify` result |
| :--- | :--- |
| Edit `.ai-context/config.toml` (`mermaid_style = true`) | ❌ "Context is fresh" |
| Edit an `ARCHITECTURE.md` embedded via `context_docs` | ❌ "Context is fresh" |
| Delete `symbols.json` | ❌ "Context is fresh"; `health` reports 0 symbols and exits 0 |

**Impact.** Breaks the central "verifiable context" promise. Configuration and embedded documents
are render inputs, but they are invisible to the content hash.

**Recommendation.** Record a render fingerprint that includes the Python content hash, the
effective configuration fingerprint, hashes of embedded context documents and the tool version;
compare it in `verify`. Track `symbols.json` as a verified artifact, and regenerate or validate it
as part of the render/health path.

### H3. Python 3.9/3.10 silently lose the default configuration

**Evidence.** `pyproject.toml:5` declares `requires-python = ">=3.9"`. The config loader uses
`tomllib` (3.11+) and falls back to `tomli` if importable
(`src/ai_context_core/analyzer/providers/config_loader.py#L21-L27`), but `tomli` is **not a declared
dependency** (the wheel requires only `click` and `rich`).

Simulating the absence of both parsers yields:

```
top-level keys: ['quality_thresholds', 'scoring']
context budget: None
sources: None
patterns: None
```

`defaults.toml` is ignored entirely, and the hardcoded fallback
(`config_loader.py#L134-L155`) contains no `context`, `sources` or `patterns` sections. The default
8,000-token budget and the `dependencies = 2500` section cap disappear.

**Impact.** A clean install on a supported Python version behaves differently from the documented
defaults. CI tests 3.10, but `tomli` is present transitively through `build`/`coverage`, masking
the defect.

**Recommendation.** Either add `tomli>=2.0; python_version < "3.11"` to `dependencies` or raise
`requires-python` to `>=3.11`. Add a clean-install CI job for the oldest supported Python.

### H4. The CI quality gate is a no-op and Ruff is not enforced

**Evidence.** `.github/workflows/ci.yml#L41` runs:

```bash
uv run ai-ctx audit --threshold 50
```

`audit` was removed in v5.0.0. The hidden redirect stub prints a notice and **exits 0**
(`src/ai_context_core/cli/commands/deprecated.py#L44-L48`). Verified: `ai-ctx audit --threshold 50`
returns exit code 0 without evaluating anything.

In addition:

- No `ruff check` or `ruff format --check` step exists in CI.
- The matrix is `["3.10", "3.11"]`, while classifiers advertise 3.9, 3.12 and 3.13.

**Impact.** The green CI badge certifies a gate that does not run, and the project's only
linter/formatter is not enforced.

**Recommendation.** Replace the `audit` step with `uv run ai-ctx context --check` (already
advertised in `README.md`) or `uv run ai-ctx verify`; add Ruff; expand the matrix or narrow the
declared classifiers.

---

## 5. Medium-severity findings

### M1. Configuration documentation describes options that do not exist

`docs/CONFIGURATION.md` documents:

- `[quality_weights]` (`docs/CONFIGURATION.md:34`) — never read anywhere in `src/`.
- `[analysis] parallel_workers`, `cache_enabled`, `max_file_size_mb`
  (`docs/CONFIGURATION.md:113-L121`) — none is consumed. In particular, no file-size guard exists:
  a very large `.py` is still read and parsed.
- The note at `docs/CONFIGURATION.md:121` claims the module cache is keyed by file hash only and
  that `--no-cache` is required after a config change. This is **incorrect**:
  `engine.py#L62-L65` computes a configuration fingerprint and `fs_cache.py#L85-L90` invalidates
  the cache when it changes. `docs/ARCHITECTURE.md:103` repeats the same error.

**Recommendation.** Implement the options or remove them from the docs; correct the cache note.

### M2. `tiktoken` is documented but not implemented

`src/ai_context_core/context/budget.py#L1-L5` and `docs/ARCHITECTURE.md:50` claim an optional
`tiktoken` accelerator selected through `[context.budget].tokenizer`. No code references
`tokenizer` or `tiktoken`; `estimate_tokens` always uses `chars / 4`.

### M3. `max_workers` is hardcoded to 8

`src/ai_context_core/analyzer/engine.py#L54`:

```python
self.max_workers = max_workers or (2 * (4 if hasattr(time, "get_clock_info") else 1))
```

`hasattr(time, "get_clock_info")` is always true, so the default is always 8. It ignores
`os.cpu_count()` and the documented `[analysis].parallel_workers`. The `import time` exists only
for this expression.

### M4. `ai-ctx init --profile` is dead

`src/ai_context_core/cli/commands/init.py#L20-L28` looks for `config/profiles/`, which does not
exist in the package (only `defaults.toml` and `loader.py`). Verified: `ai-ctx init --profile qgis`
prints "✨ Ready" without copying any configuration. `list_profiles()` can only return `generic`.

### M5. Two diverging changelogs; README links the stale one

`CHANGELOG.md` (root) includes 5.1.0. `docs/CHANGELOG.md` stops at 5.0.1 with an empty
`[Unreleased]`. `README.md:28` links to `docs/CHANGELOG.md`, so readers following the README miss
the latest release.

### M6. The "every artifact has provenance" claim is false

`README.md:38` states that every artifact carries a `_meta` block with `source`, `schema`,
`tool_version`, `git_sha` and `content_hash`. Actual state:

| Artifact | `_meta` |
| :--- | :--- |
| `project_context.json` | ✅ |
| `context_manifest.json` | ✅ |
| `AI_CONTEXT.md` | ❌ No provenance, version or `git_sha` |
| `symbols.json` | ❌ Only `{"schema": 1, ...}` |
| `PROJECT_SUMMARY.md` | ❌ Only a date and version line |

An agent reading `AI_CONTEXT.md` cannot tell which source, version or commit produced it.

### M7. `symbols.json` is neither regenerated nor verified

`ai-ctx context` does not write `symbols.json`; only `ai-ctx symbols` does. `verify` does not track
it and `health` reads it without a freshness check. With the file deleted, `health` reports
"Fresh: True" and "0 definitions, 0 references" with exit code 0.

### M8. The structure tree ignores `.analyzerignore`

`build_structure` calls `fs_tree.generate_tree_optimized`
(`src/ai_context_core/analyzer/providers/fs_tree.py#L8`), which applies a fixed exclusion list and
does **not** use the project `IgnoreFilter`. As a result, the committed artifacts include `dist/`
(with stale 5.0.1 wheels), `.coverage` and `.ai_context_cache.json`, although `.analyzerignore`
excludes them from analysis. In addition:

- If the external `tree` binary exists, its output is truncated to 1,500 characters **without a
  marker**, and it differs from the internal fallback (which hides dotfiles and limits each
  directory to 8 files). The structure section therefore depends on the host.
- On this machine `tree` is absent, so the fallback was used.

### M9. `PROJECT_SUMMARY.md` embeds a timestamp

`src/ai_context_core/analyzer/builders/reporting.py#L112` adds `Analysis Date: <now>` to the
`MarkdownBuilder` used by `ProjectSummaryGenerator`. Every `analyze` run produces a different file
even when nothing changed.

### M10. v4 residue in `builders/issues.py`

`src/ai_context_core/analyzer/builders/issues.py#L11-L29` still reads the `security` and `debt`
keys, domains removed by the v5 context-only contract (ADR-0008). Only the circular-dependency
branch remains functional.

---

## 6. Low-severity findings and hygiene

- **Unused parameter**: `ResultsAggregator.aggregate(..., _qgis_metadata)` is unused
  (`builders/aggregator.py#L39`); the call site passes `{}` (`engine.py#L95`).
- **Duplicate work**: `detect_unused_imports_in_project` runs without config in
  `builders/dependencies.py#L107` and again with config in the aggregator.
- **Wrong exception type**: `verify.py#L64-L67` catches `OSError`, but `relative_to` raises
  `ValueError` for paths outside the project.
- **Locale-dependent encoding**: `DependencyAnalyzer._read_file` uses `read_text(errors="ignore")`
  without `encoding` (`builders/dependencies.py#L125-L127`).
- **Git without timeout**: `providers/runner.py#L18` runs `git` without a timeout; a hung command
  blocks analysis (the tree helper does use a 3-second timeout).
- **Tautological condition**: `if ext in self.COMMON_EXTS or ext:` at
  `providers/fs_scanner.py#L111` is always true for files with an extension; `COMMON_EXTS` is
  therefore meaningless. A leftover `# DEBUG:` comment remains at line 119.
- **Over-broad test detection**: `is_test_file` uses `"test" in path.parent.name.lower()`, which
  classifies files in directories such as `contest/` as tests.
- **Side effects in JSON mode**: `ai-ctx analyze --format json` still writes `AI_CONTEXT.md`,
  `project_context.json` and `context_manifest.json` (`cli/commands/analyze.py#L30-L50`).
- **Inspection commands bypass sources**: `stats`, `deps`, `git`, `graph`, `roadmap` and `help-me`
  instantiate `ProjectAnalyzer` directly; `--source external` only affects `analyze`/`context`.
- **No logging configuration**: `logger.info/warning` is never emitted because logging is not
  configured, and there is no `-v` flag.
- **Metric literals outside the contract**: `builders/metrics_summarizer.py#L41` uses
  `"max_complexity"` and `visitors/ast_metrics.py#L67` uses `"total_functions"` outside
  `metric_keys`.
- **Stale user documentation**: `docs/user_guide/QUICK_START.md` and `PROFILES_GUIDE.md` mention
  removed `audit`/`doctor` commands; `docs/PATTERNS_DETECTION.md` documents removed pattern
  detection.
- **Tracked scratch files**: `ai-context-core-patch.md` and `ai_ctx_bug_report.md` at the repository
  root; `docs/bug_report_v320.md` and `docs/maintenance/bug_report_v320.md` are duplicates that
  differ.
- **Stale local bytecode**: `__pycache__` contains `.pyc` files for modules that no longer exist
  (`exceptions.py`, `scaffold.py`, `patterns.py`, ...). They are ignored by Git but indicate runs
  with an older tree.

---

## 7. Strengths

- **Clear layered architecture**: CLI → pipeline → sources → builders; AST visitors are pure and
  do not perform I/O.
- **Pluggable source protocol**: `AnalysisProvider` + `AnalysisResult`/`Provenance` make the
  `builtin`/`external` swap clean.
- **Correct and well-tested token budget/manifest**: the invariant
  `total == header + sum(sections)` is covered by 12 tests.
- **Cache correctness**: the cache is versioned and configuration-fingerprinted (despite the
  documentation saying otherwise).
- **Test suite**: 196 tests, 89% coverage, no placeholder assertions.
- **No dangerous constructs**: no `shell=True`, `eval`, `exec`, insecure `yaml.load` or unsafe
  `pickle`; `subprocess` is limited to `git` and `tree`.
- **Packaging**: the lockfile is consistent and the wheel ships the configuration and templates.

---

## 8. Prioritized action plan

| Priority | Action | Key files |
| :--- | :--- | :--- |
| **P0** | Sort parallel results by path; add a determinism regression test | `analyzer/providers/worker.py`, `analyzer/builders/aggregator.py` |
| **P0** | Extend the `verify` fingerprint: config + embedded docs + `symbols.json` | `context/verify.py`, `cli/commands/context_ops.py` |
| **P0** | Declare `tomli` for `<3.11` or raise `requires-python`; clean-install CI job | `pyproject.toml`, `analyzer/providers/config_loader.py` |
| **P0** | Replace the `audit` CI step with `context --check`; add Ruff; expand the matrix | `.github/workflows/ci.yml` |
| **P1** | Documentation truth pass: remove or implement `[quality_weights]`/`[analysis]`; fix the cache note; unify the changelog | `docs/CONFIGURATION.md`, `docs/ARCHITECTURE.md`, `README.md`, `CHANGELOG.md` |
| **P1** | Add provenance to `AI_CONTEXT.md`/`symbols.json` or correct the README claim | `analyzer/builders/ai_context_generator.py`, `context/symbol_index.py` |
| **P1** | Generate and verify `symbols.json` in the render path | `cli/commands/context_ops.py`, `context/health.py` |
| **P1** | Derive `max_workers` from CPU/config; remove `import time` | `analyzer/engine.py` |
| **P1** | Remove v4 residue (`security`/`debt`) and dead profile code | `analyzer/builders/issues.py`, `cli/commands/init.py` |
| **P2** | Deterministic tree that respects `.analyzerignore`, with a truncation marker | `analyzer/providers/fs_tree.py` |
| **P2** | Make `PROJECT_SUMMARY.md` reproducible (no timestamp or `SOURCE_DATE_EPOCH`) | `analyzer/builders/reporting.py` |
| **P2** | Hygiene: `ValueError`, explicit encoding, git timeout, scratch files, duplicate docs | multiple |

---

## 9. Appendix — reproducible checks

```bash
# Test suite and coverage
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q --cov=ai_context_core --cov-report=term-missing

# Quality gates
UV_CACHE_DIR=/tmp/uv-cache uv run ruff check .
UV_CACHE_DIR=/tmp/uv-cache uv run ruff format --check .
UV_CACHE_DIR=/tmp/uv-cache uv lock --check

# CLI health
UV_CACHE_DIR=/tmp/uv-cache uv run ai-ctx stats
UV_CACHE_DIR=/tmp/uv-cache uv run ai-ctx verify
UV_CACHE_DIR=/tmp/uv-cache uv run ai-ctx health

# Determinism experiment (disposable copy)
rsync -a --exclude .git --exclude .venv ./ /tmp/acc-copy/
UV_CACHE_DIR=/tmp/uv-cache uv run ai-ctx context --path /tmp/acc-copy --no-cache
sha256sum /tmp/acc-copy/AI_CONTEXT.md
# repeat and compare
```

---

## 10. Remediation status (2026-10-19)

The P0 findings were fixed after this audit was written:

- **H1**: module results are sorted by path at the worker/aggregator boundary, and a
  byte-stability regression test renders a >5-module fixture twice.
- **H2**: `verify` now records and checks a `render_fingerprint` covering sources,
  effective configuration, embedded context documents and tool version;
  `symbols.json` carries and validates a source `content_hash`.
- **H3**: `tomli` is declared for Python `<3.11`, and CI runs a clean runtime
  install on Python 3.9.
- **H4**: CI runs Ruff, executes `ai-ctx verify`, and covers Python 3.9–3.13.

Remaining work: the P1/P2 items (documentation truth pass, provenance in
`AI_CONTEXT.md`, generic deterministic tree, summary timestamp, v4 residue).

---

*Independent audit of the pre-remediation state. See §10 for fixes applied
afterwards.*
