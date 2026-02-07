# Profiles Guide

`ai-context-core` uses a powerful profile system to adapt its analysis to different types of Python projects. A "Profile" defines the rules, thresholds, and patterns that the analyzer looks for.

## 📂 Profile Location

Built-in profiles are located in `src/ai_context_core/config/profiles/`.
User-defined profiles can be created in your project's `.ai-context/profiles` directory.

## 📝 Anatomy of a Profile

A profile is a YAML file with three main sections:

### 1. `quality_weights`
Defines how much each metric contributes to the overall "Quality Score" (0-100) of a file.

| Metric | Weight | Condition |
| :--- | :--- | :--- |
| `no_syntax_error` | 25 | The file has no critical syntax errors. |
| `complexity_low` | 20 | Cyclomatic complexity is below the low threshold. |
| `docstrings` | 15 | Modules, classes, and functions have Google-style docstrings. |
| `size_small` | 15 | Physical line count is below the small threshold. |
| `complexity_medium` | 10 | Cyclomatic complexity is within the medium range. |
| `size_medium` | 10 | Physical line count is within the medium range. |
| `has_main` | 5 | The file includes an execution entry point (`if __name__ == "__main__":`). |
| `complexity_high` | -10 | Penalty for excessive cyclomatic complexity. |

### 2. `quality_thresholds`
Define the boundaries for metrics. These are configurable per profile to adapt to different project scales (e.g., microservices vs. large monoliths).

| Threshold | Default (TOML) | Description |
| :--- | :--- | :--- |
| **Complexity** | 10 (Warning), 15 (Error) | Cyclomatic complexity per module. |
| **Maintainability** | 65 (Warning), 50 (Error) | Maintainability Index based on Halstead/Volume. |
| **Lines (SLOC)** | 400 (Warning), 800 (Error)| Lines of code excluding empty/comments. |

> [!NOTE]
> When using `ai-ctx audit`, the tool will exit with code 1 if any module reaches the **Error** threshold.

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

3.  **Active via TOML**:
    In your `.ai-context/config.toml`, reference the profile or override values directly:
    ```toml
    [analysis]
    profile = "my-api-profile"
    ```

## 🛠️ CLI & Profile Integration

### Verifying Configuration (`doctor`)
Use the `doctor` command to verify that your profile is loaded correctly and that there are no syntax errors in your TOML overrides.
```bash
ai-ctx doctor
```

### Profile-Driven Scaffolding
The `scaffold` command uses weights and thresholds from the active profile to generate code that is "compliant by design". If your profile enforces a complexity limit of 10, the generated templates will be optimized for that constraint.

### Automated Fixes (`fix`)
The `fix` command can synchronize versions and metadata based on your profile's `project_metadata` settings, ensuring that your `__init__.py` and `pyproject.toml` are always in sync with the profile expectations.
