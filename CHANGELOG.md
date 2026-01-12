
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
