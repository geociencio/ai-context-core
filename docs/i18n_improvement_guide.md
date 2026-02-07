# i18n String Detection Improvement Guide

This document details the current state of i18n string detection in `ai-context-core` and proposes technical improvements to reduce false positives and enhance the precision of the QGIS Compliance Score.

## 1. Current State (v3.1.x)

The detection logic resides in `ai_context_core/analyzer/qgis_checkers/i18n_components/string_utils.py`. The `is_translatable_string` function uses the following heuristics:

- **Exclusion Filters**: Ignores empty strings, single characters, paths (`/`, `./`, `\\`), URLs (`http://`), and technical placeholders (`{}`).
- **Inclusion Criteria**: Accepts strings containing **spaces** or specific punctuation (`.,!?;`).
- **Context Awareness**: The `I18nChecker` automatically ignores strings inside:
    - Loggers (`debug`, `info`, `warning`, etc.).
    - Standard Exceptions (`ValueError`, `RuntimeError`, etc.).
    - Technical Qt/QGIS methods (`setObjectName`, `addItem`, etc.).

---

## 2. Weak Points Identified

1.  **Technical Dictionaries**: Configuration collections (e.g., `{"key": "Technical Value"}`) are detected as UI strings if the value contains a space.
2.  **Attribute Names**: Short strings with punctuation (e.g., `"data.value"`) are occasionally misidentified.
3.  **AST Context Depth**: The current analyzer sometimes sees the `ast.Constant` in isolation, without full knowledge of whether it's a dictionary key or a technical function argument.
4.  **Complex Technical Strings**: Default QGIS layer names or styles (e.g., `"Single Symbol"`) might inflate the total string count without being actual translatable application content.

---

## 3. Implemented & Proposed Strategies

### A. Completed Victories (v3.1.2)
- ✅ **Standard Metadata**: Strict validation of `metadata.txt`.
- ✅ **Common Method Filtering**: Integrated a wide list of technical methods to ignore during scan.
- ✅ **Naming Pattern Heuristics**: Added logic to ignore `snake_case`, `camelCase`, and `UPPER_CASE` technical identifiers.

### B. Future Improvements (Roadmap)
- **Manual Opt-out (no-i18n)**: Support inline comments like `ERROR_CODE = "technical.err" # no-i18n` to manually exclude strings.
- **Entropy Analysis**: Technical strings often have a different character distribution than human language.
- **Language Detection Snippets**: Use light-weight heuristics to check if the string contains common words from a base dictionary (ES/EN).

---

## 4. Developer Workarounds

While the analyzer continues to evolve, we recommend:

1.  **Use `.analyzerignore`**: Exclude directories that do not contain UI logic (e.g., `core/validation`, `infrastructure/`).
2.  **Externalize Config**: Move technical dictionaries to external JSON/TOML files, which are usually ignored by the Python scanner.
3.  **Force tr()**: Ensure that ALL user-facing messages are wrapped in `self.tr()` or `QCoreApplication.translate()`.

---

> [!NOTE]
> This document serves as a living guide for the `ai-context-core` team to maintain high precision in QGIS compliance metrics.
