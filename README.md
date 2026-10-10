# AI Context Core

[![CI](https://github.com/geociencio/ai-context-core/actions/workflows/ci.yml/badge.svg)](https://github.com/geociencio/ai-context-core/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![GitHub Release](https://img.shields.io/github/v/release/geociencio/ai-context-core.svg)](https://github.com/geociencio/ai-context-core/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![Downloads](https://img.shields.io/pypi/dm/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Compile token-efficient, verifiable context for AI-assisted coding.**

`ai-context-core` (CLI `ai-ctx`) turns a Python project into **context
artifacts** an AI agent can consume: a structured `AI_CONTEXT.md`, a
machine-readable `project_context.json`, a token `context_manifest.json` and a
symbol index. Everything is versioned, provenance-tagged and optionally
token-budgeted.

> **Context-only contract (v5.0.0).** `ai-context-core` is a **context compiler**
> (`source → transform → render → verify`): it *consumes* analysis instead of
> owning it. QGIS compliance, i18n, security scanning and quality gates live in
> [`qgis-plugin-analyzer`](https://github.com/geociencio/qgis-plugin-analyzer);
> scaffolding in `agentic-forge`. Commands such as `audit`, `qgis`, `security`,
> `patterns`, `inspect`, `full-scan`, `fix`, `scaffold`, `doctor`, `interactive`
> and `serve` were removed (hidden redirect stubs remain for one release). See
> [ADR-0008](docs/adr/0008-context-only-contract.md),
> the [v5.0.0 plan](docs/plans/implementation_plan_ai_context_core_context_only_v5.md)
> and the [CHANGELOG](docs/CHANGELOG.md).

## Features

### Context compilation
- **Pluggable sources**: `--source auto|external|builtin`. `external` consumes
  `qgis-plugin-analyzer` output (`analysis_results/project_context.json`);
  `builtin` runs the internal AST engine. `auto` prefers external when present.
- **Hybrid by design**: structure tree, git evolution and manual notes are always
  computed by `ai-context-core`; the analysis fields come from the selected source.
- **Provenance**: every artifact carries a `_meta` block (`source`, `schema`,
  `tool_version`, `git_sha`, `content_hash`).

### Token budget & manifest
- `ai-ctx context --max-tokens N` caps `AI_CONTEXT.md` with **deterministic**
  truncation; per-section caps via `[context.budget]`.
- `context_manifest.json` records exact per-section token deltas, the budget and
  the total (`total == header + sum(sections)`).

### Verification & index
- `ai-ctx verify` exits `1` when the tracked sources changed since the last
  render (content hash); `ai-ctx context --check` gates CI.
- `ai-ctx symbols [--grep]` writes a versioned `symbols.json` (definitions and
  references with `file:line`).
- `ai-ctx health` reports freshness, token usage, symbol coverage and provenance
  — no quality gate; it fails only on staleness.

### Context analysis (builtin source)
- **Structure**: project tree, slide-of-code and file statistics.
- **Entry points**: `__main__`-guard detection.
- **Dependencies**: import graph, circular dependencies, unused imports, coupling
  (CBO), graph density/DAG, Mermaid diagram.
- **Git evolution**: hotspots and code churn.
- **Metrics**: cyclomatic complexity, Maintenance Index, type-hint coverage.

### Performance & robustness
- **Incremental cache**: hybrid `mtime` + SHA-256 file cache (`--no-cache` to bypass).
- **Smart parallelism**: sequential below a threshold, batched `ProcessPoolExecutor` above it.
- **Fast ignore**: compiled-regex file filtering via `.analyzerignore`.
- **Staleness-safe hashing**: verification bypasses the in-process read cache.

## Installation

### Using `uv` (recommended)

```bash
# As a global tool
uv tool install ai-context-core

# Or inside a virtual environment
uv venv && source .venv/bin/activate
uv pip install ai-context-core
```

### Using `pip`

```bash
pip install ai-context-core
```

*It is always recommended to use a virtual environment.*

## Quick start

```bash
# 1. Initialize the .ai-context structure (optional)
ai-ctx init

# 2. Compile context artifacts
ai-ctx context                       # AI_CONTEXT.md + project_context.json + context_manifest.json
ai-ctx context --source external     # consume qgis-plugin-analyzer output
ai-ctx context --max-tokens 8000     # enforce a token budget
ai-ctx context --check               # generate and assert freshness (CI)

# 3. Verify and inspect
ai-ctx verify                        # exit 1 if sources changed since render
ai-ctx symbols --grep my_function    # file:line index lookup
ai-ctx health                        # freshness + tokens + symbols + provenance
```

## Generated artifacts

| Artifact | Description |
| :--- | :--- |
| `AI_CONTEXT.md` | Structured, token-budgeted context for LLMs. |
| `project_context.json` | Machine-readable analysis payload + `_meta` provenance. |
| `context_manifest.json` | Per-section token counts, budget and total. |
| `symbols.json` | Versioned symbol index (definitions + references). |
| `PROJECT_SUMMARY.md` | Human-readable summary (emitted by `analyze`). |

## Configuration

Full reference: [docs/CONFIGURATION.md](docs/CONFIGURATION.md). Defaults live in
`src/ai_context_core/config/defaults.toml`.

```toml
context_docs = []                      # extra markdown to embed as architecture notes

[context]
sections = ["structure", "metrics", "dependencies", "git"]

[context.budget]
max_tokens = 8000                      # override per run with --max-tokens N
# [context.budget.sections]
# structure = 1500

[sources]
source = "auto"                        # auto | external | builtin
# external_path = "analysis_results/project_context.json"
```

### Analysis scope (`.analyzerignore`)

`ai-ctx` reads `.analyzerignore` at the project root to exclude paths from the
analysis scope (modules, dependency graph, code metrics).

> [!IMPORTANT]
> A project `.analyzerignore` **replaces** the built-in defaults; it does not
> extend them. Re-list the standard environment/packaging patterns
> (`__pycache__/`, `.git/`, `.venv/`, `build/`, `dist/`, `*.egg-info/`) if you
> still want them ignored.

## Commands reference

### Compile & verify

| Command | Description |
| :--- | :--- |
| `ai-ctx context` | Compile `AI_CONTEXT.md`, `project_context.json`, `context_manifest.json` (primary path). Options: `--source`, `--max-tokens`, `--check`, `--include-md`, `--no-cache`, `--workers`. |
| `ai-ctx analyze` | Run the pipeline and emit `AI_CONTEXT.md`, `PROJECT_SUMMARY.md`, `project_context.json`. Options: `--source`, `--format markdown\|json`, `--include-md`, `--no-cache`, `--workers`. |
| `ai-ctx verify` | Exit `1` when artifacts are stale relative to the tracked sources. |
| `ai-ctx symbols` | Build `symbols.json`; `--grep <text>` prints matching `file:line` entries. |
| `ai-ctx health` | Context freshness, token usage, symbol coverage, provenance. |

### Inspect

| Command | Description |
| :--- | :--- |
| `ai-ctx stats` | Quick project statistics (SLOC, modules, complexity, maintenance index). |
| `ai-ctx deps` | Dependency analysis: `--unused`, `--cycles`, `--metrics` (CBO, density, DAG). |
| `ai-ctx git` | Git evolution: hotspots and churn (`--days N`). |
| `ai-ctx graph` | Export the dependency model as a Mermaid diagram (`--output ARC.mmd`). |
| `ai-ctx roadmap` | Refactor priority (complexity × churn). |
| `ai-ctx compare <a> <b>` | Diff two analysis JSON reports by metric. |
| `ai-ctx help-me` | Context-health recommendations. |

### Project setup

| Command | Description |
| :--- | :--- |
| `ai-ctx init` | Create `.ai-context` config and workflow templates (`--profile <name>`). |
| `ai-ctx profiles` | List available profiles (`python-generic`). |
| `ai-ctx clean` | Remove cache and generated artifacts (`--dry-run` to preview). |

## Metrics

Metrics are heuristics computed from static analysis and are **not directly
comparable** to the canonical metrics of other tools (e.g. `qgis-analyzer`).

| Metric | Definition | Notes |
| :--- | :--- | :--- |
| **ai-ctx Quality Score** → *context health* | Aggregated 0–100 heuristic: base 100 minus penalties for average/outlier complexity, low maintainability and missing tests, plus test bonuses. Includes an explicit score breakdown. | Tool-specific; not a gate. Being reframed as **context health** (see ADR-0008). |
| **Avg Cyclomatic Complexity** | Arithmetic mean of per-module cyclomatic complexity. | An **average**; `qgis-analyzer` applies a per-function **gate** (CC ≤ 10). |
| **Avg Maintenance Index (MI)** | SEI Maintenance Index normalized to 0–100, averaged across modules. | Exclusive to `ai-context-core`. |
| **Max Complexity** | Highest single-module cyclomatic complexity. | Complements the average to surface outliers. |

## API stability and deprecations

The **canonical public API** lives under `ai_context_core.analyzer` (`engine`,
`providers`, `visitors`, `builders`), `ai_context_core.sources`,
`ai_context_core.context`, `ai_context_core.model` and
`ai_context_core.cli.commands`. Anything else is internal.

Deprecated compatibility aliases emit a `DeprecationWarning` and are scheduled
for removal in **v5.0.0** (`REMOVAL_VERSION`):

| Deprecated path | Use instead |
| :--- | :--- |
| `analyzer.builders.aggregator.ContextAggregator` | `analyzer.builders.aggregator.ResultsAggregator` |

## Docker support

Reproducible development, testing and CI via Docker:

```bash
make docker-build    # Build all images
make docker-test     # Run the test suite with coverage
make docker-shell    # Interactive development shell
make docker-lint     # Run the linter
```

## License

This project is licensed under the **GNU General Public License v3 (GPLv3)**.
See the [LICENSE](LICENSE) file for the full license text.
