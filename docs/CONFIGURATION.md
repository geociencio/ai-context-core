# Configuration Guide

`ai-context-core` allows flexible configuration via TOML files, following a "Zero External Dependencies" policy for configuration loading.

## Configuration Hierarchy

The tool loads configuration in the following order of priority (from lowest to highest):

1.  **System Defaults**: Default values compiled in `src/ai_context_core/config/defaults.toml`.
2.  **Project Configuration**: `.ai-context/config.toml` file in your project root.

Standard configuration follows the TOML format. While legacy YAML remains partially supported for backward compatibility, **TOML is now the required standard** for all new projects and profiles.

## Available Options

### 1. Quality Thresholds (`quality_thresholds`)

They define the limits for considering metrics as warnings or errors.

```toml
[quality_thresholds.complexity]
warning = 10  # Alert if cyclomatic complexity > 10
error = 15    # Fail if complexity > 15

[quality_thresholds.maintainability]
warning = 65  # Alert if MI < 65
error = 50    # Fail if MI < 50

[quality_thresholds.lines]
warning = 400 # Alert if file > 400 lines
error = 800   # Fail if file > 800 lines
```

### 2. Per-Module Scoring Weights (`quality_weights`)

Integer weights used by the per-module scorer.

```toml
[quality_weights]
docstrings = 30
complexity_low = 20
complexity_medium = 10
complexity_high = -10
size_small = 15
size_medium = 10
has_main = 5
no_syntax_error = 30
```

### 3. Project Quality Score (`scoring`)

Additive adjustments applied to a 100-point base to produce the `ai-ctx Quality Score`. Exposed in `PROJECT_SUMMARY.md` as an explicit **Score Breakdown**. All values are optional and fall back to the defaults below.

```toml
[scoring]
base_score = 100.0
complexity_medium_threshold = 15.0          # Average CC above which a penalty applies
complexity_medium_penalty_per_point = 2.0
complexity_high_threshold = 25.0            # Highest-module CC outlier threshold
complexity_high_penalty_per_point = 0.5
complexity_high_penalty_cap = 10.0
maintainability_threshold = 65.0
maintainability_penalty_per_point = 1.5
no_tests_penalty = 20.0
tests_bonus_per_file = 2.0
tests_bonus_cap = 10.0
```

### 4. Security Patterns (`security_patterns`)

Defines which functions and modules are considered dangerous by the AST scanner.

```toml
[security_patterns]
# Functions that execute dynamic code or system commands
dangerous_functions = ["exec", "eval", "__import__", "input"]

# Modules known for insecure deserialization or vulnerable protocols
dangerous_modules = ["pickle", "marshal", "telnetlib"]

# String patterns suggesting SQL Injection
sql_injection_indicators = ["execute(", "executemany("]
```

### 5. Analysis Configuration (`analysis`)

Technical parameters of the analysis engine to optimize performance.

```toml
[analysis]
parallel_workers = "auto"  # "auto" uses cores*2, or a specific integer
cache_enabled = true       # Uses persistent cache (.ai_context_cache.json)
max_file_size_mb = 10      # Ignores files larger than this limit
```

> [!NOTE]
> Incremental analysis allows subsequent runs to be near-instant if files haven't physically changed.

### 6. Context Docs (`context_docs`)

Extra markdown documents (globs relative to the project root) embedded into the
"MANUAL ARCHITECTURE NOTES" section of `AI_CONTEXT.md`. Equivalent to the
`ai-ctx analyze --include-md <glob>` CLI flag (repeatable).

```toml
context_docs = ["ARCHITECTURE.md", "docs/*.md"]
```

### 7. QGIS i18n Analysis (`patterns.i18n`)

Configures internationalization analysis for QGIS plugins. The optional
`ignored_functions` / `ui_functions` lists override the built-in technical
denylist and user-facing allowlist; omit them to use the defaults.

```toml
[patterns.i18n]
# Scope of i18n analysis
# - "all": Analyze all project files (default)
# - "gui_only": Analyze only typical GUI paths
# - "custom": Use custom include/exclude patterns
scope = "gui_only"

# Patterns used when scope = "gui_only"
gui_patterns = ["gui/**/*.py", "dialogs/**/*.py", "ui/**/*.py"]

# Custom patterns (only used when scope = "custom")
include_patterns = ["src/my_plugin/**/*.py"]
exclude_patterns = ["src/my_plugin/core/**/*.py"]

# Optional classification overrides
# ignored_functions = ["setObjectName", "addItem"]  # technical denylist
# ui_functions = ["setText", "setTitle"]            # user-facing allowlist
```

## Customization Example

Create a `.ai-context/config.toml` file to make the analysis stricter:

```toml
# .ai-context/config.toml

[quality_thresholds.complexity]
warning = 5  # Very strict, alert with any complex logic
error = 10

[scoring]
complexity_high_threshold = 15.0  # Penalize modules above CC 15

[analysis]
parallel_workers = 4
```
