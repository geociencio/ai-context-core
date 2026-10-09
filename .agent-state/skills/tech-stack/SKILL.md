---
name: tech-stack
description: Toolchain, dependency management with uv, and quality tools for ai-context-core.
trigger: when installing dependencies, configuring the environment, or running linting/formatting.
---

# Tech Stack

Defines the ecosystem of tools and libraries that sustain `ai-context-core` development.

## When to use this skill
- When installing new dependencies.
- When configuring the development environment.
- When running linting or formatting tools.
- When verifying Python version compatibility.

## Degree of Freedom
- **Strict**: `uv` as package manager is mandatory.

## Workflow
1. **Manage**: Use `uv` for any package operation.
2. **Synchronize**: Keep the environment up to date with `uv sync`.
3. **Quality**: Run `ruff` for static validation.

## Instructions and Rules

### 1. Core Technologies
- **Python**: >= 3.9
- **Manager**: `uv` (replaces pip/poetry)
- **Quality**: `ruff` (configured in `pyproject.toml`; single linter/formatter)

### 2. Dependency Management
- **Add**: `uv add [package]`
- **Dev**: `uv add --dev [package]`
- **Install**: `uv sync`

### 3. Code Quality
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Tests**: `uv run pytest -q`

## Quality Checklist
- [ ] Is `uv` prioritized?
- [ ] Are the exact ruff commands mentioned?
- [ ] Is the Python version correct?
- [ ] Are obsolete tools (pip/venv) avoided?
