# AI Context Core

[![CI](https://github.com/geociencio/ai-context-core/actions/workflows/ci.yml/badge.svg)](https://github.com/geociencio/ai-context-core/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![GitHub Release](https://img.shields.io/github/v/release/geociencio/ai-context-core.svg)](https://github.com/geociencio/ai-context-core/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![Downloads](https://img.shields.io/pypi/dm/ai-context-core.svg)](https://pypi.org/project/ai-context-core/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![QGIS Plugin Ready](https://img.shields.io/badge/QGIS-Plugin%20Ready-green?logo=qgis)](https://qgis.org)
[![AI-Context Driven](https://img.shields.io/badge/AI-Context%20Driven-blue?logo=openai)](https://github.com/geociencio/ai-context-core)

The central nervous system for your AI-assisted coding workflow.

> **Context-only (v5.0.0).** `ai-context-core` is now a **context compiler**
> (`source → transform → render → verify`): it consumes analysis instead of
> owning it. QGIS compliance, i18n, security scanning and quality gates live in
> `qgis-plugin-analyzer`; scaffolding in `agentic-forge`. The former `audit`,
> `qgis`, `security`, `patterns`, `inspect`, `full-scan`, `fix`, `scaffold`,
> `doctor`, `interactive` and `serve` commands were removed (hidden redirect
> stubs remain for one release). See [ADR-0008](docs/adr/0008-context-only-contract.md),
> the [v5.0.0 plan](docs/plans/implementation_plan_ai_context_core_context_only_v5.md)
> and the [CHANGELOG](docs/CHANGELOG.md).

## Features

### Core Capabilities
- **Context Compilation**: Extracts and renders token-efficient, versioned
  context artifacts (`AI_CONTEXT.md`, `project_context.json`) for AI agents.
- **Pluggable Sources**: `--source auto|external|builtin` — consume
  `qgis-plugin-analyzer` output or fall back to the built-in engine.
- **Context Commands**: `context`, `analyze`, `stats`, `deps`, `git`, `graph`,
  `roadmap`, `compare`, `help-me`, `init`, `profiles`, `clean`.
- **Verifiable & budgeted**: `verify` (staleness), `symbols` (index + `--grep`),
  `health` (freshness/tokens/provenance), `context --max-tokens N`,
  `context --check` for CI.
- **Profiles**: `python-generic` (the `qgis-plugin` profile moved to
  `qgis-plugin-analyzer`).

### Context Analysis
- **Entry Point Detection**: `__main__`-guard entry points.
- **Dependency Analysis**: 
    - Import graph with cycle detection
    - Unused imports identification
    - Coupling metrics (CBO - Coupling Between Objects)
    - Graph density and DAG validation
- **Git Evolution Tracking**:
    - Hotspots (most frequently modified files)
    - Code churn analysis (lines added/deleted over time)
- **Advanced Metrics**: 
    - **Maintenance Index (MI)** for code maintainability
    - **Halstead Metrics** for code complexity
    - **Cyclomatic Complexity** per module
    - **Type Hint Coverage** analysis

### Reporting & Visualization
- **Interactive HTML**: Generate interactive project summaries with `--format html`.
- **Dependency Graphs**: Automated **Mermaid.js** diagrams integrated into reports.
- **Quick Stats**: Terminal-based formatted tables using `rich` for rapid insights.
- **Multiple Formats**: Markdown, HTML, and JSON outputs for specialized data extraction.
- **Visual Analytics**: Direct terminal visualization of hotspots, churn, and architectural priorities.

### Performance & Optimization
- **FastIgnore**: Ultra-fast file filtering using compiled Regex.
- **Smart Parallelism**: Dynamic switching between sequential and parallel execution based on project size.
- **Single-Pass AST**: Unified pattern detection for maximum performance.
- **Incremental Cache**: Hybrid `mtime` and SHA-256 based file caching with `--no-cache` option.
- **Batch Processing**: Task batching in parallel mode to minimize inter-process communication overhead.

### Workflow Integration
- **CI/CD Ready**: verify context freshness and enforce token budgets (see the v5.0.0 roadmap).
- **Workflow Automation**: Standardized scripts for session management.
- **AI Recommendations**: Heuristic-based actionable advice for code hygiene.
- **Clean Command**: Automated cleanup of cache and generated artifacts.

## Installation

### Using `uv` (Recommended)

`uv` is extremely fast and the preferred way to manage this tool.

**As a global tool**:
```bash
uv tool install ai-context-core
```

**In a virtual environment**:
```bash
uv venv
source .venv/bin/activate
uv pip install ai-context-core
```

### Using `pip`

You can install `ai-context-core` using standard `pip`:

```bash
pip install ai-context-core
```

*Note: It is always recommended to use a virtual environment.*

## Configuration

For detailed configuration options, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

### Analysis Scope (`.analyzerignore`)

`ai-ctx` reads a `.analyzerignore` file at the project root to exclude paths from
the **analysis scope** (modules, dependency graph, security scan, code metrics).

> [!IMPORTANT]
> A project `.analyzerignore` **replaces** the built-in defaults; it does not
> extend them. Re-list the standard environment/packaging patterns
> (`__pycache__/`, `.git/`, `.venv/`, `build/`, `dist/`, `*.egg-info/`) if you
> still want them ignored.

Excluding `tests/` here does **not** remove the test bonus from the Quality Score:
test files are counted by a decoupled scanner that ignores `.analyzerignore`.

### QGIS i18n Analysis

Configure the scope and classification of internationalization analysis in
`.ai-context/config.toml` (or `src/ai_context_core/config/profiles/qgis.toml`):

```toml
[patterns.i18n]
# Scope: "all" (default), "gui_only", or "custom"
scope = "gui_only"

# Patterns used when scope = "gui_only"
gui_patterns = ["gui/**/*.py", "ui/**/*.py"]

# Optional overrides for string classification (omit to use the built-in lists)
# ignored_functions = ["setObjectName", "addItem"]  # technical denylist
# ui_functions = ["setText", "setTitle"]            # user-facing allowlist
```

## Commands Reference

### Core Commands

#### `ai-ctx --version`
Displays the current version of the tool.
- **Usage**: `ai-ctx --version`

#### `ai-ctx init`
Initializes the `.ai-context` structure in your project. It creates configuration files and initial prompt templates.
- **Usage**: `ai-ctx init --profile <name>`
- **Example**: `ai-ctx init --profile qgis-plugin`

#### `ai-ctx analyze`
Runs the complete analysis pipeline. Generates `AI_CONTEXT.md`, `PROJECT_SUMMARY.md/html`, and `project_context.json`.
- **Options**:
    - `--format json`: Generates a machine-readable JSON analysis for CI/CD integration.
    - `--no-cache`: Forces a full re-analysis, ignoring incremental metadata.
    - `--workers <n>`: Override automatic parallel worker calculation.
    - `--include-md <glob>`: Embed extra markdown docs (repeatable) into the
      "MANUAL ARCHITECTURE NOTES" section. Also configurable per project via the
      `context_docs` config key.
- **Usage**: `ai-ctx analyze --format json > report.json`

#### `ai-ctx profiles`
Lists all available configuration profiles.
- **Usage**: `ai-ctx profiles`

---

### Analysis Commands

#### `ai-ctx stats`
Shows quick project statistics in a formatted table. Perfect for getting a rapid overview without generating full reports.
- **Displays**:
    - Source Lines (SLOC) vs Physical Lines
    - Module, Function, and Class counts
    - Average Complexity and Maintenance Index
    - Quality Score
    - Top 5 most complex modules
- **Usage**: `ai-ctx stats`

#### `ai-ctx deps`
Analyzes project dependencies with detailed insights.
- **Options**:
    - `--unused`: Shows all unused imports across the project
    - `--cycles`: Detects circular dependencies
    - `--metrics`: Displays coupling metrics (CBO, graph density, DAG status)
    - *(No flags = shows all)*
- **Usage**: 
    ```bash
    ai-ctx deps --unused
    ai-ctx deps --cycles
    ai-ctx deps --metrics
    ai-ctx deps  # Shows everything
    ```

#### `ai-ctx git`
Shows git evolution analysis including hotspots and code churn.
- **Options**:
    - `--days <n>`: Number of days for churn analysis (default: 30)
- **Displays**:
    - Most frequently modified files (hotspots)
    - Lines added/deleted in the specified period
    - Total code churn
- **Usage**: `ai-ctx git --days 30`

---

### Context & Maintenance Commands

#### `ai-ctx help-me`
Provides context-health recommendations (missing architecture notes, git history, structure).
- **Usage**: `ai-ctx help-me`

#### `ai-ctx clean`
Cleans cache and generated artifacts from the project directory.
- **Options**:
    - `--dry-run`: Preview what would be deleted without actually deleting
- **Removes**:
    - `.ai_context_cache.json`
    - `AI_CONTEXT.md`
    - `project_context.json`
    - `PROJECT_SUMMARY.md` and `PROJECT_SUMMARY.html`
    - `ANALYSIS_REPORT.md`
- **Usage**: 
    ```bash
    ai-ctx clean --dry-run  # Preview
    ai-ctx clean            # Actually delete
    ```

---

### Exploration Commands

#### `ai-ctx graph`
Architectural visualization tool. Exports the project's internal dependency model to a Mermaid-formatted file.
- **Usage**: `ai-ctx graph --output ARC.mmd`

#### `ai-ctx compare <file1> <file2>`
Regression tracking utility. Compares two JSON reports and highlights deltas in metrics and complexity.
- **Usage**: `ai-ctx compare base.json current.json`

#### `ai-ctx roadmap`
Technical debt prioritization engine. Calculates a "Refactor Score" based on (Code Complexity × Churn Frequency) to identify high-risk hotspots.
- **Usage**: `ai-ctx roadmap`

## Metrics

`ai-context-core` reports its own set of metrics. These are heuristics computed from static analysis and are **not directly comparable** to the canonical metrics of other tools (e.g. `qgis-analyzer`).

| Metric | Definition | Notes |
| :--- | :--- | :--- |
| **ai-ctx Quality Score** → *context health* (v5.0.0) | Aggregated 0-100 heuristic: base 100 minus penalties for average/outlier complexity, low maintainability, and missing tests, plus test bonuses. The report includes an explicit score breakdown. | Tool-specific; not comparable to `qgis-analyzer`'s Quality Score. Being renamed to **context health** in v5.0.0 (see ADR-0008). |
| **Avg Cyclomatic Complexity** | Arithmetic mean of per-module cyclomatic complexity. | This is an **average**. `qgis-analyzer` applies a per-function **gate** (CC ≤ 10), so the two numbers mean different things. |
| **Avg Maintenance Index (MI)** | SEI Maintenance Index normalized to 0-100, averaged across modules. | Exclusive to `ai-context-core`. |
| **Max Complexity** | Highest single-module cyclomatic complexity. | Complements the average to surface outliers. |

## Comparison with Other Tools

`ai-context-core` is more than a code packager; it is a **deep static intelligence engine** designed to maximize context fidelity for LLMs. While many tools focus on "repository dumping," we focus on **semantic extraction** and **domain-specific hygiene**.

### How It Differs

| Aspect | `ai-context-core` |
| :--- | :--- |
| **Primary Goal** | **Compile context** (`source → transform → render → verify`), not analyze. |
| **Sources** | `qgis-plugin-analyzer` output (external) or a built-in AST fallback. |
| **Outputs** | `AI_CONTEXT.md`, `project_context.json` (with `_meta` provenance). |
| **Analysis Depth** | Delegated: hygiene, QGIS, i18n, security and CC gates live in `qgis-plugin-analyzer`. |
| **Git Awareness** | Hotspots / churn, rendered into the context. |
| **Dependencies / Graph** | Import graph, unused imports, coupling, Mermaid diagram. |
| **Language Scope** | Python. |

> **Scope note:** `ai-context-core` is a **consumer** of analysis. By design it no longer
> performs security scanning, QGIS/i18n compliance, design-pattern detection or quality
> gates — those are owned by `qgis-plugin-analyzer`. It focuses on producing compact,
> versioned, provenance-tagged context artifacts for AI agents.

### Why `ai-context-core`?

#### 1. Pluggable Context Compilation
Point it at `qgis-plugin-analyzer` output (`--source external`) or let it run its built-in
engine (`--source builtin`); either way you get the same rendered context with provenance
recorded in `project_context.json`.

#### 2. Clean Ecosystem Boundaries
Hygiene (QGIS, i18n, security, quality gates) is single-sourced in
`qgis-plugin-analyzer`; scaffolding in `agentic-forge`. `ai-context-core` stays focused on
the context it compiles.

#### 3. Actionable Technical Debt Identification
By combining **Git Churn/Hotspots** with **Cyclomatic Complexity**, the `ai-ctx roadmap` command surfaces "Biological Debt"—files that are both complex and frequently modified. This guides your AI assistant to the most critical areas for refactoring.

#### 4. Security-First Context
Our integrated security scan detects **SQL Injection**, **Insecure Calls**, and **Hardcoded Secrets** using context-aware AST analysis, ensuring that the code you provide to an LLM is not only readable but also safe and compliant.

### When to Choose
✅ **Choose ai-context-core** for professional Python/QGIS development, deep architectural audits, pre-release quality gates, and high-fidelity AI pairing where structural context is critical.

❌ **Choose Alternatives** for quick, one-off code dumps (Gitingest), real-time interactive terminal editing (Aider), or simple multi-language packaging (Repomix).

## API Stability and Deprecations

The **canonical public API** lives under `ai_context_core.analyzer` (`engine`,
`providers`, `visitors`, `builders`) and `ai_context_core.cli.commands`. Anything
else is considered internal.

The following legacy paths are **deprecated compatibility facades**. They still
work but emit a `DeprecationWarning` on import and are scheduled for removal in
**v4.0.0**:

| Deprecated path | Use instead |
| :--- | :--- |
| `ai_context_core.analyzer.patterns_detectors.*` | `ai_context_core.analyzer.visitors.*` (`analyzer.pattern_base` for `base`) |
| `ai_context_core.analyzer.context_builders.*` | `ai_context_core.analyzer.builders.*` |
| `ai_context_core.commands.*` | `ai_context_core.cli.commands.*` |
| `ai_context_core.cli_groups.*` | `ai_context_core.cli.commands.*` |
| `ContextAggregator` alias | `ResultsAggregator` |
| `QGISComplianceVisitor` alias | `GenericQGISComplianceVisitor` |

## Docker Support

The project includes Docker support for reproducible development, testing, and CI/CD.

### Quick Start with Docker

```bash
# Build all images
make docker-build

# Run tests in Docker
make docker-test

# Interactive development shell
make docker-shell

# Run linter
make docker-lint
```

### Docker Images

- **Development** (`ai-ctx:dev`) - Full environment with dev dependencies
- **Test** (`ai-ctx:test`) - Runs test suite with coverage
- **Production** (`ai-ctx:prod`) - Minimal runtime image

---
Generated by Ai-Context-Core v3.5.0

## License

This project is licensed under the **GNU General Public License v3 (GPLv3)**. See the [LICENSE](LICENSE) file for the full license text.
