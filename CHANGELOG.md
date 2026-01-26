
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Docker Support**: Multi-stage Dockerfile with development, test, and production images
- **Docker Compose**: Services for development, testing, and linting
- **Makefile Targets**: Added `docker-build`, `docker-test`, `docker-lint`, `docker-shell`, `docker-clean`

### Changed
- **Workflows**: Enhanced all session workflows with Agent Actions and validation criteria
  - `inicia-sesion`: Added context prioritization and Docker support
  - `cierra-sesion`: Added code formatting, historical archiving, and mandatory session reports
  - `crea-el-comit`/`create-commit`: Added AI-assisted commit message generation
- **CLI Commands**: Fixed workflow commands to use correct module path
- **Code Formatting**: Applied black formatter to entire codebase (11 files reformatted)

### Documentation
- **README**: Added comprehensive Docker usage section
- **Session Reports**: Created structured session documentation in `docs/sessions/`
- **Next Steps**: Implemented historical archiving system for development continuity
- **Architecture Decision Records (ADR)**: Established ADR process with template and initial records
  - Created `docs/adr/` directory with README and template
  - ADR-0001: Decision to use ADRs for architecture decisions
  - ADR-0002: Decision to implement 13 improvements roadmap in 4 phases
- **Improvement Planning**: Comprehensive roadmap for ai-context-core enhancements
  - Analysis report identifying 13 critical improvements
  - Implementation plan with 4 phases (43-52 hours for phases 1-3)
  - Executive summary with ROI analysis and success metrics
  - Detailed task breakdown with checkboxes for tracking
  - Documentation index for easy navigation


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
