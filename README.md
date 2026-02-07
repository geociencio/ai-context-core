# AI Context Core

The central nervous system for your AI-assisted coding workflow.

## Features

### Core Capabilities
- **Project Analysis**: Deep AST analysis for Python projects with SLOC calculation (excluding comments/docstrings).
- **Context Management**: Keeps `.ai-context` files updated for AI-assisted development.
- **14 CLI Commands**: Comprehensive toolset for analysis, inspection, and maintenance.
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
- **Multiple Formats**: Markdown, HTML, and JSON outputs.

### Performance & Optimization
- **FastIgnore**: Ultra-fast file filtering using compiled Regex.
- **Smart Parallelism**: Dynamic switching between sequential and parallel execution based on project size.
- **Single-Pass AST**: Unified pattern detection for maximum performance.
- **Incremental Cache**: SHA-256 based file caching with `--no-cache` option to force full re-analysis.

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
    - `--format html`: Generates an interactive HTML report.
    - `--no-cache`: Forces a full re-analysis of all files.
    - `--workers <n>`: Number of parallel workers for analysis.
- **Usage**: `ai-ctx analyze --format html`

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

## Comparison with Other Tools

`ai-context-core` is unique because it combines **deep AST-based static analysis** with **workflow automation** and **specialized domain support**. Here's how it compares to other tools in the modern ecosystem (2024-2025):

### Context & Analysis Matrix

| Feature | `ai-context-core` | `Repomix` | `Code2Prompt` | `Aider` | `pyqgis4-checker` | `Ruff` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary Goal** | **Context + Hygiene** | **Code Packager** | **Prompt Builder** | **AI Pair Programming** | **Qt6 Migration** | **Fast Linting** |
| **AST Analysis** | ✅ Deep (Patterns/SLOC) | ❌ None | ❌ None | ⚠️ Repo Map | ✅ Specific | ⚠️ Basic |
| **Pattern Detection**| ✅ Native (5 Patterns) | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **QGIS Auditing** | ✅ i18n/Processing | ❌ No | ❌ No | ❌ No | ✅ Qt6 Specific | ❌ No |
| **Security Audit** | ✅ Deep (SQLi/Secrets) | ❌ No| ❌ No | ❌ No | ❌ No | ⚠️ Basic |
| **Git Awareness** | ✅ Hotspots/Churn | ❌ No | ✅ Yes | ✅ Deep | ❌ No | ❌ No |
| **Reporting** | ✅ HTML/JSON/Markdown | ✅ XML/JSON/MD | ✅ XML/JSON/MD | ❌ In-Chat | ❌ Console | ❌ Console |
| **Incremental Cache**| ✅ SHA-256 | ❌ No | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| **Zero Dependencies** | ✅ Core Analysis | ✅ Yes | ⚠️ Minimal | ❌ Many | ⚠️ Dependencies | ✅ Yes |

### Unique Differentiators

#### 1. Deep Semantic Extraction (vs. Code Packagers)
While tools like **Repomix** and **Code2Prompt** are excellent for "packing" your code for an LLM, `ai-context-core` extracts **semantic meaning**. We don't just dump text; we analyze the AST to identify:
- **Design Patterns**: Singleton, Factory, Strategy, Observer, Decorator.
- **Architectural Issues**: God Objects, Spaghetti Code, High Coupling (CBO).
- **Security Flaws**: Insecure calls, SQL injections, and hardcoded secrets.

#### 2. Domain-Specific Intelligence (QGIS & Qt)
Unlike generic analysis tools, we have deep roots in the **QGIS ecosystem**. We provide:
- **i18n Compliance**: Tracking `self.tr()` coverage across your plugin.
- **Qt6 Migration**: Identifying PyQt5 vs PyQt6 discrepancies to prepare for QGIS 4.0.
- **Processing Framework**: Validating algorithm structure and metadata.

#### 3. LLM-Agnostic "Source of Truth"
Tools like **Aider** or **Cody** are tied to specific agents or models. `ai-context-core` provides a standalone, high-fidelity context that you can feed into **any** AI (Claude, GPT, Gemini, DeepSeek) or use for automated audits in CI/CD without model-specific locks.

#### 4. Actionable Technical Debt Tracking
By combining **Git metrics** (Churn/Hotspots) with **Static analysis** (Complexity/MSI), we identify the most critical files to refactor—the "Biological Debt" of your project—guiding your AI assistant to where it matters most.

### When to Choose `ai-context-core`

✅ **Perfect for**:
- Preparing codebases for AI-assisted development
- CI/CD quality gates with the `audit` command
- QGIS plugin development (specialized compliance checks)
- Understanding legacy codebases (patterns, dependencies, hotspots)
- Security audits before code reviews
- Tracking technical debt over time

❌ **Not ideal for**:
- Real-time AI pair programming (use `aider` or `cursor`)
- Simple code formatting (use `black` or `ruff`)
- Language-agnostic analysis (we're Python-focused)

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
Generated by Ai-Context-Core
