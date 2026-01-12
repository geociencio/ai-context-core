
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Tests**: Initial unit test suite for analyzer modules (`ast_utils`, `fs_utils`, `issues`).
- **Docs**: Quick start guide for users.

### Changed
- **Analyzer Refactoring**: Reduced cyclomatic complexity in `fs_utils.py` and `ast_utils.py` by extracting helper functions.
- **Security Logic**: Modularized security pattern scanning in `issues.py` to separate pattern definition from execution.
- **Code Quality**: Fixed bare `except` blocks and improved detection of false positives in security scanning.

## [0.1.0] - 2026-01-11

### Added
- **Core Engine**: Initial release of the modular analysis engine.
- **CLI**: `ai-ctx` command line interface with `init` and `analyze` commands.
- **Profiles**: Support for configurable analysis profiles (Generic, QGIS Plugin).
- **Workflows**: Standardized workflow templates for AI-assisted development (`inicia-sesion`, `crea-el-comit`).
- **AST Analysis**: Static analysis capabilities for metrics, types, and docstrings.
- **Dependency Graph**: Graph-based dependency analysis and cycle detection.
