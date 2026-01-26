# Changelog

# DEVELOPMENT LOG

## [2026-01-25] Modularización Completa y Reducción de Deuda Técnica
- **Resumen**: Se completó la transformación del proyecto de una base procedimental a una arquitectura 100% modular basada en clases.
- **Resultado**: El Quality Score se mantuvo sobre 71 y se eliminaron ~1,400 líneas de código duplicado. Los tests (65/65) están pasando en Docker.
- **Contexto**: Este hito cierra el ciclo de limpieza profunda y prepara la base para visualizaciones avanzadas.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2026-01-26 - Major Architectural Upgrade & Advanced CLI

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

### Added
- **Advanced QGIS Heuristics**: 
    - Full detection of **QGIS Processing Framework** (Algorithms and Providers).
    - **i18n Coverage**: Automated validation of `self.tr()` and `translate()` usage.
    - **Qt6 Transition Audit**: Proactive detection of PyQt5 imports and legacy SIGNAL/SLOT macros to prepare for QGIS 4.
    - **Architecture Notes**: Integration of manual documentation from `.ai-context/architecture_notes.md` into final reports.
- **Strict Metadata Validation**: Rigorous checker for `metadata.txt` adhering to official QGIS.org standards.

### Fixed
- **CLI Robustness**: Fixed a critical `KeyError` in `ai-ctx patterns` and `ai-ctx security` caused by missing heuristic keys in the analyzer results.

### Optimized
- **FastIgnore Engine**: High-performance file filtering system using compiled Regex (linear speedup).
- **Smart Parallelism**: Dynamic execution engine that chooses between sequential and parallel processing based on codebase size to eliminate IPC overhead.
- **Single-Pass Pattern Detection**: Unified all architectural detectors into a single `ast.NodeVisitor` pass, reducing AST traversal overhead by ~60%.
- **High-Efficiency Cache**: Refactor of `LRUCache` to use `OrderedDict`, achieving consistent $O(1)$ performance for eviction and lookups.

## [Unreleased]

## [1.0.1] - 2026-01-22

### Fixed
- **Configuration**: Fixed missing `defaults.yaml` and templates in installed package by adding `MANIFEST.in` and updating `pyproject.toml`.

## [1.0.0] - 2026-01-11

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

### Added
- **Core Engine**: Initial release of the modular analysis engine.
- **CLI**: `ai-ctx` command line interface with `init` and `analyze` commands.
- **Profiles**: Support for configurable analysis profiles (Generic, QGIS Plugin).
- **Workflows**: Standardized workflow templates for AI-assisted development (`inicia-sesion`, `crea-el-comit`).
- **AST Analysis**: Static analysis capabilities for metrics, types, and docstrings.
- **Dependency Graph**: Graph-based dependency analysis and cycle detection.
