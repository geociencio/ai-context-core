# Configuration Guide

`ai-context-core` allows flexible configuration via TOML files, following a "Zero External Dependencies" policy for configuration loading.

## Configuration Hierarchy

The tool loads configuration in the following order of priority (from lowest to highest):

1.  **System Defaults**: Default values compiled in `src/ai_context_core/config/defaults.toml`.
2.  **Project Configuration**: `.ai-context/config.toml` file in your project root.
3.  **Profile Configuration**: `.yaml` files in `.ai-context/config.yaml` (Legacy/Transition).

> [!TIP]
> It is recommended to use `.ai-context/config.toml` for all new configurations.

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

### 2. Scoring Weights (`quality_weights`)

They determine how the final "Quality Score" (0-100) is calculated. The sum should be approx 1.0.

```toml
[quality_weights]
complexity = 0.25       # 25% Cyclomatic Complexity
maintainability = 0.20  # 20% Maintainability Index
test_coverage = 0.15    # 15% Test Coverage
documentation = 0.15    # 15% Docstring Quality
security = 0.25         # 25% Absence of Security Vulnerabilities
```

### 3. Security Patterns (`security_patterns`)

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

### 4. Analysis Configuration (`analysis`)

Technical parameters of the analysis engine to optimize performance.

```toml
[analysis]
parallel_workers = "auto"  # "auto" uses cores*2, or a specific integer
parallel_batch_size = 10   # Groups files in batches to reduce IPC overhead
cache_enabled = true       # Uses persistent cache (.ai_context_cache.json)
incremental = true         # Ultra-fast checking via mtime/size before hashing
max_file_size_mb = 10      # Ignores files larger than this limit
```

> [!NOTE]
> Incremental analysis allows subsequent runs to be near-instant if files haven't physically changed.

## Customization Example

Create a `.ai-context/config.toml` file to make the analysis stricter:

```toml
# .ai-context/config.toml

[quality_thresholds.complexity]
warning = 5  # Very strict, alert with any complex logic
error = 10

[quality_weights]
# Prioritize security above everything else
security = 0.50
complexity = 0.20
maintainability = 0.10
documentation = 0.10
test_coverage = 0.10

[analysis]
parallel_workers = 4
```
