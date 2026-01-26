# Profiles Guide

`ai-context-core` uses a powerful profile system to adapt its analysis to different types of Python projects. A "Profile" defines the rules, thresholds, and patterns that the analyzer looks for.

## 📂 Profile Location

Built-in profiles are located in `src/ai_context_core/config/profiles/`.
User-defined profiles can be created in your project's `.ai-context/profiles` directory.

## 📝 Anatomy of a Profile

A profile is a YAML file with three main sections:

### 1. `quality_weights`
Defines how much each metric contributes to the overall "Quality Score" (0-100) of a file. The score is calculated by summing the weights of all met conditions.

Here are the available metrics and their default weights:

| Metric              | Default Weight | Description                                            |
|---------------------|----------------|--------------------------------------------------------|
| `docstrings`        | 30             | The file has a docstring.                              |
| `complexity_low`    | 20             | The cyclomatic complexity is low.                      |
| `size_small`        | 15             | The file size is small.                                |
| `has_main`          | 5              | The file has a `if __name__ == "__main__":` block.     |
| `no_syntax_error`   | 30             | The file has no syntax errors.                         |
| `complexity_medium` | 10             | The cyclomatic complexity is medium.                   |
| `complexity_high`   | -10            | The cyclomatic complexity is high.                     |
| `size_medium`       | 10             | The file size is medium.                               |

### 2. `thresholds`
Define the boundaries for metrics. What is "too complex" or "too large" depends on the project type.

Here are the available thresholds and their default values:

| Threshold           | Default Value | Description                                               |
|---------------------|---------------|-----------------------------------------------------------|
| `complexity_low`    | 5             | Cyclomatic complexity below this value is considered low.   |
| `complexity_medium` | 15            | Cyclomatic complexity below this value is considered medium.|
| `complexity_high`   | 25            | Cyclomatic complexity below this value is considered high.  |
| `size_small`        | 200           | File size (in lines) below this value is considered small.|
| `size_medium`       | 500           | File size (in lines) below this value is considered medium.|

### 3. `patterns`
Enables or disables specific detection logic modules.

Here are the available patterns:

| Pattern             | Description                                                   |
|---------------------|---------------------------------------------------------------|
| `qgis_compliance`   | Rules specific to QGIS plugin development.                    |
| `linter`            | Integration with Ruff for linting.                            |

## 🚀 Creating a Custom Profile

1.  Create a new YAML file in your project's `.ai-context/profiles` directory, e.g., `my-profile.yaml`.
2.  Define your overrides (you don't need to copy everything, just what changes from `defaults.yaml`).

**Example `my-profile.yaml`**:
```yaml
profile_name: "my-api-profile"
description: "A strict profile for a Flask-based microservice."

quality_weights:
  docstrings: 40
  complexity_low: 30
  complexity_high: -20

thresholds:
  complexity_high: 10
  size_small: 100

patterns:
  qgis_compliance:
    enabled: false
```

3.  Use it via CLI:
    ```bash
    ai-ctx init --profile my-api-profile
    ```
    The tool will automatically find your custom profile.
