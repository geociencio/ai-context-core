---
name: i18n-standards
description: Internationalization standards for the analyzer itself — tr(), translate(), and the # no-i18n opt-out.
trigger: when modifying the i18n visitor, auditing translations, or extending i18n heuristics.
---

# i18n Standards — ai-context-core

> Standards and best practices for internationalization in the ai-context-core codebase.

## When to Use
- When auditing or fixing i18n-related code in the analyzer itself.
- When extending the `I18nChecker` with new wrapper patterns or heuristics.
- When changing `is_translatable_string` classification.

## Core Principles

### 1. The Analyzer Audits i18n — It Must Set the Standard
As a tool that audits QGIS plugins for i18n compliance, the analyzer's own code must follow the same standards it enforces.

### 2. Recognized i18n Wrappers
The `I18nChecker` (`visitors/i18n.py`) recognizes:
- `self.tr("...")` — standard QObject translation.
- `QCoreApplication.translate("Context", "...")` — Qt API for non-QObject contexts.
- `translate("...")` — bare translate wrapper.

### 3. Opt-out
Strings annotated with `# no-i18n` are skipped by the checker (detected via `tokenize` line mapping in `visitors/i18n_components.py`).

## Heuristic Reference

`is_translatable_string()` (`visitors/i18n_components.py`):
- Requires length ≥ 3 characters.
- Skips paths (`/`, `\`) and dict keys.
- Skips snake_case, camelCase, PascalCase, UPPERCASE identifiers.
- Skips punctuation-dominated strings.
- Skips strings inside ignored function calls (logging, exceptions).

## Testing i18n Changes
1. Add cases to `tests/test_i18n_opt_out.py` and `tests/test_qgis_compliance.py`.
2. Run `uv run pytest tests/test_i18n_opt_out.py tests/test_qgis_compliance.py -q`.
3. Run self-audit: `uv run ai-ctx analyze .`.

## Known Limitations
- The checker matches `tr`/`translate` by function name only, not full dotted path.
- Short UI strings (`OK`, `Save`) are not flagged due to heuristic filters.
- Docstrings are excluded.
