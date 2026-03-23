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

## Features

### Core Capabilities
- **Project Analysis**: Deep AST analysis for Python projects with SLOC calculation (excluding comments/docstrings).
- **Context Management**: Keeps `.ai-context` files updated for AI-assisted development.
- **20+ CLI Commands**: Comprehensive toolset for analysis, inspection, and maintenance.
- **Profiles**: 
    - `python-generic`: Standard Python support.
    - `qgis-plugin`: Specialized rules for QGIS plugin development, including:
        - **Processing Framework** validation.
        - **i18n (self.tr)** coverage metrics.
        - **Qt6/QGIS 4** transition audit.
        - **metadata.txt** strict validation.

### Advanced Analysis
- **Entry Point Detection**: Supports QGIS plugins, Click CLIs, Flask, and FastAPI apps.
- **Anti-Pattern Detection**: Identifies God Objects, Spaghetti Code, Magic Numbers, and Dead Code.
- **Design Pattern Detection**: Native support for **Strategy**, **Singleton**, **Observer**, **Factory**, and **Decorator** patterns.
- **Security Audit**: Scans for vulnerabilities like SQL Injection, `eval/exec`, and Secrets detection with false-positive filtering.
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
- **CI/CD Ready**: `audit` command with configurable quality thresholds and exit codes.
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

### QGIS i18n Analysis (New in v3.2.0)

Configure the scope of internationalization analysis in your project's `.ai-context/config.toml` (or `src/ai_context_core/config/profiles/qgis.toml`):

```toml
[qgis.i18n]
# Scope: "all" (default), "gui_only", or "custom"
scope = "gui_only"

# Patterns used when scope = "gui_only"
gui_patterns = ["gui/**/*.py", "ui/**/*.py"]
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
- **Usage**: `ai-ctx analyze --format json > report.json`

#### `ai-ctx profiles`
Lists all available configuration profiles.
- **Usage**: `ai-ctx profiles`

---

### Analysis Commands

#### `ai-ctx inspect <file>`
Performs a deep, granular analysis of a **single Python file**. Ideal for checking metrics and security for a specific module without running the full project analysis.
- **Usage**: `ai-ctx inspect src/my_script.py`

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

### Specialized Commands

#### `ai-ctx patterns`
Displays a clean, tabulated view of all **Design Patterns** detected across the project (Singleton, Factory, Observer, Strategy, Decorator).
- **Usage**: `ai-ctx patterns`

#### `ai-ctx security`
Executes a **security-focused scan**. It only runs checks for SQL injections, Secrets, and insecure code patterns, making it extremely fast.
- **Usage**: `ai-ctx security`

#### `ai-ctx qgis`
Validates QGIS plugin compliance and readiness.
- **Validates**:
    - `metadata.txt` according to QGIS.org standards
    - Internationalization (i18n) coverage with `self.tr()`
    - Qt6/QGIS 4 transition readiness (PyQt5 vs PyQt6 imports)
    - Processing Framework usage
    - Overall QGIS Compliance Score
- **Usage**: `ai-ctx qgis`

#### `ai-ctx help-me`
Provides a prioritized list of **AI Recommendations** generated by our heuristic engine. It focuses purely on actionable quality improvements.
- **Usage**: `ai-ctx help-me`

---

### CI/CD & Maintenance Commands

#### `ai-ctx audit`
A utility designed for **CI/CD pipelines**. It calculates the project's Quality Score and exits with code 1 if it falls below the specified threshold.
- **Options**:
    - `--threshold <value>`: Minimum score required (default: 70)
- **Usage**: `ai-ctx audit --threshold 85`

#### `ai-ctx serve`
Starts a local HTTP server to view the interactive `PROJECT_SUMMARY.html` report in your browser.
- **Options**:
    - `--port <number>`: Port to use (default: 8000)
    - `--open`: Opens the browser automatically
- **Usage**: `ai-ctx serve --open`

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

### Maintenance & Exploration Commands

#### `ai-ctx doctor`
Environmental diagnostics utility. Checks Python compatibility, configuration consistency, and project structure alignment.
- **Usage**: `ai-ctx doctor --path .`

#### `ai-ctx fix`
Automated remediation for common issues.
- **Fixes**: Missing `__init__.py` files, linting errors (via Ruff), and version synchronization.
- **Options**: `--sync-version` (Aligns `__init__.py` with `pyproject.toml`)
- **Usage**: `ai-ctx fix --sync-version`

#### `ai-ctx graph`
Architectural visualization tool. Exports the project's internal dependency model to a Mermaid-formatted file.
- **Usage**: `ai-ctx graph --output ARC.mmd`

#### `ai-ctx compare <file1> <file2>`
Regression tracking utility. Compares two JSON reports and highlights deltas in quality, complexity, and security metrics.
- **Usage**: `ai-ctx compare base.json current.json`

#### `ai-ctx scaffold <pattern>`
Design pattern generator. Bootstraps standards-compliant code templates for architectural patterns.
- **Supported**: Strategy, Observer (more coming soon).
- **Usage**: `ai-ctx scaffold strategy -o my_strategy.py`

#### `ai-ctx roadmap`
Technical debt prioritization engine. Calculates a "Refactor Score" based on (Code Complexity × Churn Frequency) to identify high-risk hotspots.
- **Usage**: `ai-ctx roadmap`

## Comparison with Other Tools

`ai-context-core` is more than a code packager; it is a **deep static intelligence engine** designed to maximize context fidelity for LLMs. While many tools focus on "repository dumping," we focus on **semantic extraction** and **domain-specific hygiene**.

### Detailed Comparison Matrix (2024-2025)

| Feature | `ai-context-core` | `Repomix` | `Aider` | `Gitingest` | `Code2Prompt` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Primary Goal** | **Context + Hygiene** | **Code Packaging** | **AI Pair Progr.** | **Quick Digest** | **Prompt Builder** |
| **Analysis Depth**| **Deep AST** (Semantics) | Tree-sitter (Basic) | Repo Map (Signatures) | Plain Text | Plain Text |
| **Pattern Detection**| ✅ **Native (5 Patterns)** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Anti-Patterns** | ✅ God Object/Spaghetti | ❌ No | ❌ No | ❌ No | ❌ No |
| **Quality Metrics** | ✅ **CC, MI, Halstead** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Security Audit** | ✅ **Deep (SQLi/Secrets)** | ⚠️ Basic (Secrets) | ❌ No | ❌ No | ❌ No |
| **Git Awareness** | ✅ **Hotspots/Churn** | ❌ No | ⚠️ Basic Diffs | ❌ No | ✅ Yes |
| **Domain Logic** | ✅ **QGIS/Qt6 Specialists** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Reporting** | ✅ HTML/JSON/Markdown | ✅ XML/JSON/MD | ❌ In-Chat | ❌ Console | ✅ XML/JSON/MD |
| **Performance** | ✅ Parallel + SHA Cache | ✅ Fast | ✅ Incremental | ✅ Web-Speed | ✅ Rust-Based |

### Why Choose `ai-context-core`?

#### 1. Deep Semantic Understanding vs. Simple Packaging
Tools like **Repomix** and **Gitingest** are excellent for "packing" your code into a single file. However, `ai-context-core` goes further by extracting **architectural meaning**. We identify **Design Patterns** (Singleton, Factory, etc.) and calculate **Maintenance Index (MI)**, allowing the AI to understand the *why* behind your code structure, not just the *what*.

#### 2. Domain-Specific Intelligence (QGIS & Qt6)
We are the only tool with first-class support for the **QGIS ecosystem**.
- **i18n Tracking**: Real-time coverage of `self.tr()` strings.
- **Qt6 Migration**: Automated auditing for PyQt5 to PyQt6 transitions (essential for QGIS 4.x).
- **Processing Framework**: Structural validation of QGIS algorithms.

#### 3. Actionable Technical Debt Identification
By combining **Git Churn/Hotspots** with **Cyclomatic Complexity**, we identify "Biological Debt"—files that are both complex and frequently modified. This guides your AI assistant to the most critical areas for refactoring.

#### 4. Security-First Context
Our integrated security scan detects **SQL Injection**, **Insecure Calls**, and **Hardcoded Secrets** using context-aware AST analysis, ensuring that the code you provide to an LLM is not only readable but also safe and compliant.

### When to Choose
✅ **Choose ai-context-core** for professional Python/QGIS development, deep architectural audits, pre-release quality gates, and high-fidelity AI pairing where structural context is critical.

❌ **Choose Alternatives** for quick, one-off code dumps (Gitingest), real-time interactive terminal editing (Aider), or simple multi-language packaging (Repomix).

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
Generated by Ai-Context-Core v3.3.0

## License

This project is licensed under the **GNU General Public License v3 (GPLv3)**. See the [LICENSE](LICENSE) file for the full license text.
