# AI-Context-Core Development Guide

This document provides technical guidelines for extending and maintaining **AI-Context-Core**.

## 🛠️ Development Environment

- **Python**: 3.10+ (compatible up to 3.14).
- **Package Manager**: `uv` is mandatory for dependency management and running the tool during development.
- **Environment Setup**:
  ```bash
  uv sync
  source .venv/bin/activate
  ```

## 📐 Design Principles

1.  **AST-First Analysis**: All code analysis must be performed using the Abstract Syntax Tree. Avoid regular expressions for code understanding.
2.  **Stateless Visitors**: Analysis logic (`visitors/`) must be stateless to remain thread/process safe.
3.  **Command Decoupling**: Business logic must never depend on CLI-specific types (like `click.Context`). Use `ActionHandlers` to bridge them.
4.  **Zero GUI Dependencies**: This is a headless tool. Dependencies on `PyQt` or `qgis.gui` are strictly prohibited in the core engine.

## 🏗️ Extending the Tool

### Adding a New AST Detector (Visitor)
1.  **Create Visitor**: Add a new class in `src/ai_context_core/analyzer/visitors/` inheriting from `ast.NodeVisitor`.
2.  **Registry**: Register your detector in `src/ai_context_core/analyzer/registry.py` using the `@register_detector` decorator.
3.  **Data Structure**: Ensure findings are returned as serializable dictionaries.

### Adding a New CLI Command
1.  **Define Command**: Add a new function in `src/ai_context_core/cli/commands/` decorated with `@click.command()`.
2.  **Action Handler**: Implement the logic in a separate handler class to maintain testability.
3.  **Registration**: Import and add the command to the main group in `src/ai_context_core/cli/__init__.py`.

## 🧪 Testing and Verification

### Unit Testing
We use `pytest`. All new features must include unit tests in the `tests/` directory.
```bash
# Run all tests
uv run pytest

# Run with coverage target
uv run pytest --cov=src/ai_context_core
```

### Docker Verification
For environment-independent verification:
```bash
# Build and run tests in a clean container
make docker-test
```

## 📈 Quality Standards

- **Linting & Formatting**: We use `ruff` and `black`.
  ```bash
  uv run ruff check --fix .
  uv run black .
  ```
- **Complexity**: Keep cyclomatic complexity per function **below 15**.
- **Docstrings**: All public functions and classes must have Google-style docstrings.
- **Commit Messages**: Follow **Conventional Commits** (e.g., `feat(analyzer): add new cyclo detector`).

## 🔄 Release Workflow

1.  Update version in `pyproject.toml`.
2.  Add release notes to `CHANGELOG.md`.
3.  Run `uv run ai-ctx audit` to ensure quality thresholds.
4.  Use `/release-package` agent workflow for automated tagging and building.

---
**Version**: 3.1.2 | **License**: GPL v3 | **Ref**: [ARCHITECTURE.md](ARCHITECTURE.md)
