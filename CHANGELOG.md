# Changelog

# DEVELOPMENT LOG

## [2026-01-25] Modularización Completa y Reducción de Deuda Técnica
- **Resumen**: Se completó la transformación del proyecto de una base procedimental a una arquitectura 100% modular basada en clases.
- **Resultado**: El Quality Score se mantuvo sobre 71 y se eliminaron ~1,400 líneas de código duplicado. Los tests (65/65) están pasando en Docker.
- **Contexto**: Este hito cierra el ciclo de limpieza profunda y prepara la base para visualizaciones avanzadas.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.2] - 2026-02-07 - Architectural Stabilization & Global Localization
### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **CLI Suite Expansion**:
    - `ai-ctx doctor`: Environmental diagnostics and health checks.
    - `ai-ctx fix`: Auto-remediation for linting and project structure.
    - `ai-ctx graph`: Architecture visualization (Mermaid diagrams).
    - `ai-ctx roadmap`: Technical debt prioritization (Complexity × Churn).
    - `ai-ctx scaffold`: Design pattern code generation.
    - `ai-ctx compare`: Snapshot-based regression tracking.
- **Reporting**: Added `--format json` to `ai-ctx analyze` for structured data extraction.
- **Design Pattern Standardization**: Unified detector hierarchy and improved rule modularization.
- **Component Consolidation**: Merged singleton and observer logic into cohesive rule sets.

### Changed
- **Performance Optimization**: 
    - Incremental analysis using `mtime` and `size` to avoid redundant hashing.
    - Parallel processing task batching to reduce IPC overhead.
    - Optimized `fs_scanner` for large-scale directory traversal.

### Fixed
- **FS Utilities**: Restored missing facade exports in `fs_utils.py`.
- **Linting**: Updated pre-commit configurations and resolved new Ruff rules.

- [x] Test Coverage Boost: Achieved **98%** project-wide test coverage (263 tests), covering all critical modules including `engine`, `fs_utils`, `dependencies`, and `checkers`.
- [x] System Stability: Implemented comprehensive edge case handling for filesystem operations, complexity calculations, and dependency analysis.
- [x] **Documentation Localization Sprint**: Translated and modernized all core technical guides to English, establishing a universal documentation standard (v3.1.2 baseline).
    - **Updated**: `README.md`, `CONFIGURATION.md`, `PATTERNS_DETECTION.md`.
    - **Modernized**: `PROFILES_GUIDE.md`, `QUICK_START.md`, `ARCHITECTURAL_ANALYSIS.md`.
    - **Localized**: `AGENTIC_IMPLEMENTATION_GUIDE.md`, `i18n_improvement_guide.md`, `DEVELOPMENT_LOG.md`.

## [3.1.1] - 2026-02-07 - QGIS Profile & Analysis Fixes

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Integration Tests**: Added `tests/test_qgis_command.py` to verify the full QGIS compliance command flow.

### Fixed
- **QGIS Profile Enforcement**: Fixed critical bug where the `qgis` command failed to load its specialized profile, resulting in a default 0.0 compliance score.
- **Worker Execution**: Resolved `AttributeError` in `fs_utils.py` by correctly exporting `read_file_fast`, fixing silent analysis failures.
- **i18n Heuristics**: Refined translatable string detection to be more resilient to short mock strings in tests.


## [3.1.0] - 2026-02-07 - Quality Excellence & Extreme Fragmentation

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **README Update**: Integrated a comprehensive comparison matrix featuring contemporary tools like **Repomix**, **Code2Prompt**, and specialized QGIS checkers.
- **New Modular Components**: 
    - `observer_components/`: Granular logic for Observer pattern detection.
    - `singleton_components/`: Refined rules for Singleton identification.
    - `builder_components/`: Separated graph resolution from path mapping.
    - `i18n_components/`: Specialized string and call handling for QGIS analysis.
    - `import_visitor_components/`: Modularized import extraction and unused detection.
    - `issues_components/`: Fragmented registry and specialized scanners (Secrets, Debt, Optimizations).
    - `ignore_components/`: Separated pattern loading and regex compilation.

### Changed
- **Architectural Excellence (Phase 4)**: Applied extreme fragmentation to reduce all project module complexities to **< 15** (Source directory maximum: 14).
- **Quality Metrics**: 
    - Achieved record **90.4/100 Quality Score**.
    - Achieved **60.6 Average Maintenance Index**.
- **Facade Patterns**: Transformed `imports.py`, `i18n.py`, `singleton.py`, `observer.py`, `issues.py`, `ignore_filter.py`, and `import_visitor.py` into clean facades for modular components.

### Fixed
- **SLOC Accuracy**: Refined SLOC calculation by extracting specialized docstring range detection.
- **Git Analysis Parsing**: Modularized `GitParser` for better maintainability and error handling.

## [3.0.3] - 2026-02-07 - i18n Precision & Heuristic Refinement

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **QGIS Compliance Tests**: New unit tests for i18n aggregation and heuristic validation (`tests/test_qgis_compliance.py`).

### Fixed
- **i18n Aggregation**: Now correctly sums both `tr()` and `translate()` calls in QGIS compliance analysis.
- **i18n Heuristics**: 
    - Dramatically reduced false positives in string counting by ignoring logger calls (`debug`, `info`, etc.) and common exceptions (`ValueError`, `TypeError`, etc.).
    - Improved filtering of technical strings like paths, URLs, and pure placeholders (`{}`).
    - Excluded single-character strings from the translatable count.

## [3.0.2] - 2026-02-07 - Python 3.14 Compatibility & Analyzer Logic Fixes

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Python 3.14 Compatibility**: Safely handle the removal of `ast.Str` in Python 3.14 by using `ast.Constant` as a fallback in SLOC calculation.
- **Regression Tests**: Added dedicated tests for AST metrics compatibility on latest Python versions.

### Fixed
- **Complexity Calculation**: Fixed critical logical bug where `try` and `async with` blocks were double-counted in cyclomatic complexity analysis.
- **QGIS i18n Scoring**: 
    - Resolved `KeyError` when analyzing `QCoreApplication.translate` calls.
    - Optimized string counting to exclude docstrings from the total string count, preventing unfair score dilution.
    - Added heuristic to skip obvious internal IDs/keys in string enumeration.
- **Recursive Ignore Filter**: Fixed `IgnoreFilter` failure to detect files inside ignored directories during certain traversal modes; now recursively checks all path segments.
- **Legacy Fallbacks**: Removed redundant `_simple_complexity` fallback in favor of central `ComplexityVisitor`.

## [3.0.1] - 2026-01-30 - QGIS Metadata Patch

### Fixed
- **QGIS Metadata Display**: Resolved critical bug where `ai-ctx qgis` command displayed "N/A" for metadata fields despite valid validation. Field access logic in CLI was corrected to match parsed structure.

## [3.0.0] - 2026-01-30 - CLI Expansion & Enhanced Analysis

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **5 New CLI Commands**:
  - `ai-ctx deps`: Dependency analysis (unused imports, cycles, coupling metrics)
  - `ai-ctx git`: Git evolution tracking (hotspots, code churn)
  - `ai-ctx stats`: Quick project statistics with formatted tables
  - `ai-ctx qgis`: QGIS plugin compliance validation
  - `ai-ctx clean`: Cache and artifact cleanup utility
- **Rich Table Formatting**: Terminal output now uses `rich` library for beautiful formatted tables
- **Dependency Analysis Features**:
  - Import graph with cycle detection
  - Unused imports identification across the project
  - Coupling Between Objects (CBO) metrics
  - Graph density and DAG validation
- **Git Evolution Tracking**:
  - Hotspots analysis (most frequently modified files)
  - Code churn metrics (lines added/deleted over time periods)

### Changed
- **README.md**: Completely reorganized with 5 feature subsections and expanded comparison table
- **Feature Documentation**: Added comprehensive documentation for all 14 CLI commands
- **Comparison Table**: Expanded to include 6 tools (repo2txt, code2prompt, aider, radon, pylint) with 13 characteristics
- **CLI Organization**: Commands now grouped into Core, Analysis, Specialized, and CI/CD categories

### Fixed
- **Git Repository Detection**: Fixed `GitAnalyzer.is_repo()` false positives by changing `check=False` to `check=True`
- **Test Robustness**: Improved `test_is_git_repo` using mocking for environment independence

### Breaking Changes
- **Major Version Bump**: Significant CLI expansion warrants v3.0.0
- All existing commands remain backward compatible


## [2.1.3] - 2026-01-30 - SLOC Engine & Metadata Fix

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **SLOC Engine**: New `calculate_sloc` function in `ast_metrics` to accurately count code excluding docstrings/comments.
- **Reporting**: Reports now display both "Source Lines (SLOC)" and "Total Physical Lines".

### Fixed
- **QGIS Metadata**: Resolved `configparser` error when `metadata.txt` already contained a `[general]` header (implemented `strict=False`).
- **Security Tests**: Restored `issues.detect_ast_security_issues` alias for backward compatibility with test suites.
- **AI Recommendations**: Standardized result dictionary keys (`category`) to prevent `KeyError` in visualizers.

### Changed
- **Quality Metrics**: `Maintenance Index` now uses SLOC instead of raw line count for better accuracy.
- **Docstring Coverage**: Major documentation push reaching 95% coverage across core analyzer components.

## [2.1.2] - 2026-01-30 - Engine Liquidity & Quality Peak

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **aggregator.py**: New module dedicated to project-level results aggregation and post-processing.
- **Compatibility Layers**: Restored legacy API support in `ast_utils`, `issues`, `dependencies`, and `git_analysis` using modern facades.

### Changed
- **Engine Refactoring**: Deep cleanup of `engine.py`, transforming it into a high-level orchestrator.
- **Metrics Alignment**: Synchronized `defaults.toml` weights with `ProjectScorer` implementation.
- **Quality Score**: Reached record 62.3/100 score on the project's own analysis.

### Fixed
- **Stability**: Resolved multiple `AttributeError` and `KeyError` issues caused by module fragmentation.
- **CBO Metrics**: Fixed coupling calculation in `dependencies.py`.

## [2.1.1] - 2026-01-26 - Major Architectural Upgrade & Advanced CLI

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Full Modularization**: Complete refactor of all 18 core modules into class-based, decoupled architectures across 6 phases.
- **Improved Metrics Engine**: Centralized quality logic in `ProjectScorer`.
- **Strategy Prompting**: Multi-model LLM support in `AIContextManager`.
- **Final Modularization**: Deep refactor of `reporting.py` and `patterns.py` into class-based section generators and detectors.
- **Major Refactoring**: Deep refactor of `ast_utils.py`, `dependencies.py`, `fs_utils.py`, and `engine.py` to reduce complexity and improve modularity.
- **HTML Reporting**: New `--format html` option to generate interactive project summaries.
- **Advanced CLI**: Added specialized subcommands: `inspect`, `serve`, `audit`, `patterns`, `security`, and `help-me`.
- **Mermaid Diagrams**: Visual dependency graphs integrated into Markdown and HTML reports.
- **AI Recommendations**: Heuristic engine (`ai_recommendations.py`) for automated quality and maintenance advice.
- **Secret Filtering**: Logic to ignore common placeholders ("change_me", "example") in security scans.
- **Incremental Cache**: Implementation of persistent cache with `--no-cache` support to force re-analysis.
- **Testing Standards**: New agent skill and workflow to standardize testing with Pytest and Docker.
- **Maintenance Index (MI)**: Comprehensive maintainability scoring for modules and project level.
- **Git Analysis**: Native integration to detect Hotspots and monitor Code Churn over time.
- **Design Patterns**: New detection module supporting Singleton, Factory, Observer, Strategy, and Decorator patterns.
- **Advanced Dependencies**: Implemented CBO (Coupling Between Objects) metrics and smart detection of unused imports.
- **Multi-Framework**: Added support for Django (Settings, URLs, Applications), Flask, and FastAPI entry points.
- **Core Analyzer**: New `is_entry_point` detection for QGIS, Click, Flask, and FastAPI apps.
- **Anti-Patterns**: Created detection module for God Objects, Spaghetti Code, Magic Numbers, and Dead Code.
- **Security**: Enhanced AST-based security scanning for asserts and SQL injections.
- **Docker Support**: Multi-stage Dockerfile with development, test, and production images.
- **Docker Compose**: Services for development, testing, and linting.
- **Makefile Targets**: Added `docker-build`, `docker-test`, `docker-lint`, `docker-shell`, `docker-clean`.

### Changed
- **Hotspot Refactoring**: Major refactor of `ast_utils.py`, `engine.py`, and `reporting.py` to reduce complexity.
- **Workflow**: Updated `run-tests` to default to `make docker-test`.
- **Workflows**: Enhanced all session workflows with Agent Actions and validation criteria.
  - `inicia-sesion`: Added context prioritization and Docker support.
  - `cierra-sesion`: Added code formatting, historical archiving, and mandatory session reports.
  - `crea-el-comit`/`create-commit`: Added AI-assisted commit message generation.
- **CLI Commands**: Fixed workflow commands to use correct module path.
- **Code Formatting**: Applied black formatter to entire codebase.

### Documentation
- **README**: Added comprehensive Docker usage section.
- **Session Reports**: Created structured session documentation in `docs/sessions/`.
- **Next Steps**: Implemented historical archiving system for development continuity.
- **Architecture Decision Records (ADR)**: Established ADR process with template and initial records.
- **Improvement Planning**: Comprehensive roadmap for ai-context-core enhancements.

## [2.5.0] - 2026-01-26 - Performance & GIS Edition

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Advanced QGIS Heuristics**: 
    - Full detection of **QGIS Processing Framework** (Algorithms and Providers).
    - **i18n Coverage**: Automated validation of `self.tr()` and `translate()` usage.
    - **Qt6 Transition Audit**: Proactive detection of PyQt5 imports and legacy SIGNAL/SLOT macros to prepare for QGIS 4.
    - **Architecture Notes**: Integration of manual documentation from `.ai-context/architecture_notes.md` into final reports.
- **Strict Metadata Validation**: Rigorous checker for `metadata.txt` adhering to official QGIS.org standards.

### Fixed
- **CLI Robustness**: Fixed a critical `KeyError` in `ai-ctx patterns` and `ai-ctx security` caused by missing heuristic keys in the analyzer results.

## [2.5.2] - 2026-01-26 - Bugfix Real Release

### Fixed
- **KeyError 'class'**: Fixed a critical crash in `SummaryGenerator` and `AICtxGenerator` when processing patterns without a class name. This fix was intended for v2.5.1 but was not correctly included in that release's code.

## [2.5.1] - 2026-01-26 - Failed Release (Bugfix Edition)

### Fixed
- **KeyError 'class'**: (Partial/Incomplete) Initial attempt at fixing the reporting crash. Release was invalid due to missing source code updates.

## [3.2.1] - 2026-02-07 - Internationalization & Performance Peak
### Added
- **License Formalization**: Officially consolidated the project license under **GNU General Public License v3 (GPLv3)**.
- **Documentation Modernization**: Rewrote and localized all core technical guides (`ARCHITECTURE.md`, `DEVELOPMENT_GUIDE_EN.md`, etc.) to match the internal modular architecture and established **ADR 0006**.
- **Metric Aggregation**: Added "Total Physical Lines" to project-level metrics and reports (Markdown/HTML) to improve documentation density analysis.
### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Facade Elimination**: Removed all backward compatibility facade files from the `analyzer` package root, successfully migrating 266 tests and CLI commands to the modular structure.

### Added
- New `patterns_detectors/` package for modular design pattern detection.
- `ignore_filter.py` module extracted from `fs_utils.py` for better separation of concerns.

### Added
- **Configuration**: Unit tests for config system and full documentation in `docs/CONFIGURATION.md`.
- **CI/CD**: GitHub Actions workflow for automated testing and quality auditing.
- **Workflows**: Optimized local workflows (`inicia-sesion`, `cierra-sesion`) with hybrid Docker/uv support.

### Fixed
- **i18n Scope Analysis**: Fixed critical bugs in v3.2.0 where i18n configuration was ignored in aggregation, and recursive path matching (`**`) failed. Implemented high-performance regex-based matching with caching.
- **CLI QGIS Command**: Added missing `--i18n-scope` option and improved reporting transparency (active scope and analyzed module count).
- **Engine**: Resolved `KeyError: complexity` in summary generation for errored files.
- **Linting**: Fixed import order and unused variables across `analyzer` modules.
- **Clean Code**: Removed legacy garbage content from `dependencies.py`.

### Refactored
- **Modular Architecture**: Extracted 6 specialized modules from `analyzer` package (`complexity_visitor.py`, `import_visitor.py`, `html_builder.py`, `summary_generator.py`, `pattern_utils.py`, `constants.py`) reducing complexity in `reporting.py` (-267 lines, -30%) and `ast_utils.py` (-200 lines, -44%).
- **Constants Centralization**: Eliminated magic numbers by centralizing 75 configuration constants across 11 categories (complexity, quality, security, QGIS, git, patterns, etc.).
- **Backward Compatibility**: Added wrapper functions in `ast_utils.py` to preserve public API for `calculate_complexity()`, `extract_imports()`, and `detect_unused_imports()`.

### Fixed
- **DecoratorDetector**: Fixed `KeyError 'class'` by standardizing result structure to use `'class'` key consistently across all pattern detectors.

### Optimized
- **FastIgnore Engine**: High-performance file filtering system using compiled Regex (linear speedup).
- **Smart Parallelism**: Dynamic execution engine that chooses between sequential and parallel processing based on codebase size to eliminate IPC overhead.
- **Single-Pass Pattern Detection**: Unified all architectural detectors into a single `ast.NodeVisitor` pass, reducing AST traversal overhead by ~60%.
- **High-Efficiency Cache**: Refactor of `LRUCache` to use `OrderedDict`, achieving consistent $O(1)$ performance for eviction and lookups.



## [1.0.1] - 2026-01-22

### Fixed
- **Configuration**: Fixed missing `defaults.yaml` and templates in installed package by adding `MANIFEST.in` and updating `pyproject.toml`.

## [1.0.0] - 2026-01-11

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Docstrings**: Fully standardized all core modules to Google Style (98.2% coverage).
- **Security**: Added advanced obfuscation and false positive reduction for security scanning.
- **Licensing**: Added GPL-3.0-or-later license and professional PyPI metadata.
- **Tests**: Initial unit test suite for analyzer modules (`ast_utils`, `fs_utils`, `issues`).
- **Docs**: Comprehensive Release Workflow and AI documentation.

### Changed
- **Analyzer Refactoring**: Major modularization of `fs_utils.py`, `ast_utils.py`, and `engine.py`.
- **Localization**: Full translation of CLI, reports, and logs to English.
- **Technical Debt**: Reduced cyclomatic complexity across all core modules.

## [0.1.0] - 2026-01-11

### Refactored
- **Analyzer Architecture**: Restructured the analyzer into specialized `visitors`, `builders`, and `providers` packages for better maintainability and scalability.
- **Backward Compatibility**: Implemented facade-based compatibility layer to support legacy imports and ensure 100% test pass rate.

### Added
- **Core Engine**: Initial release of the modular analysis engine.
- **CLI**: `ai-ctx` command line interface with `init` and `analyze` commands.
- **Profiles**: Support for configurable analysis profiles (Generic, QGIS Plugin).
- **Workflows**: Standardized workflow templates for AI-assisted development (`inicia-sesion`, `crea-el-comit`).
- **AST Analysis**: Static analysis capabilities for metrics, types, and docstrings.
- **Dependency Graph**: Graph-based dependency analysis and cycle detection.
