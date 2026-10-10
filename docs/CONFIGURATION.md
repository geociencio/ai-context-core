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

### 3. Project Quality Score (`scoring`) — context-only note

Additive adjustments applied to a 100-point base to produce the internal
`quality_score` heuristic (reported by `ai-ctx stats`/`analyze`). In the v5.0.0
**context-only** contract this surface is being renamed to **context health**
(no quality gate); canonical quality gates live in `qgis-plugin-analyzer`.
Values are optional and fall back to the defaults below.

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

### 4. Analysis Source (`sources`)

```toml
[sources]
source = "auto"   # auto | external | builtin
# external_path = "analysis_results/project_context.json"
```

`auto` prefers `qgis-plugin-analyzer` output when present, else the built-in
engine. The former `qgis` profile was removed in v5.0.0. Security, i18n and QGIS
compliance analysis are owned by `qgis-plugin-analyzer`; `ai-context-core`
consumes their output (see `docs/adr/0008-context-only-contract.md`).

### 5. Context Rendering (`context`)

Controls `AI_CONTEXT.md`: which sections render, whether the Mermaid diagram is
styled, and the token budget.

```toml
[context]
# Renderable sections: structure, metrics, dependencies, git.
sections = ["structure", "metrics", "dependencies", "git"]

# Append Mermaid ``classDef``/``class`` styling lines to the dependency diagram.
# Off by default: the unstyled diagram is far smaller and stays legible to LLMs.
mermaid_style = false

# Token budget. ``max_tokens`` caps the whole document (override per run with
# ``ai-ctx context --max-tokens N``); ``[context.budget.sections]`` adds
# per-section caps. Remove a key (or set it to 0) to disable that cap.
[context.budget]
max_tokens = 8000
[context.budget.sections]
dependencies = 2500
```

### 6. Analysis Configuration (`analysis`)

Technical parameters of the analysis engine to optimize performance.

```toml
[analysis]
parallel_workers = "auto"  # "auto" uses cores*2, or a specific integer
cache_enabled = true       # Uses persistent cache (.ai_context_cache.json)
max_file_size_mb = 10      # Ignores files larger than this limit
```

> [!NOTE]
> Incremental analysis allows subsequent runs to be near-instant if files haven't physically changed. After editing configuration, run with `--no-cache` once because the module cache is keyed by file hash, not config.

### 7. Context Docs (`context_docs`)

Extra markdown documents (globs relative to the project root) embedded into the
"MANUAL ARCHITECTURE NOTES" section of `AI_CONTEXT.md`. Equivalent to the
`ai-ctx analyze --include-md <glob>` CLI flag (repeatable).

```toml
context_docs = ["ARCHITECTURE.md", "docs/*.md"]
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
