---
name: tech-stack
description: Technology stack guidelines and requirements
trigger: python, uv, ruff, dependencies, install
---

# Technology Stack

## Core Technologies
- **Python**: >= 3.9
- **Package Manager**: `uv` (replaces pip/poetry/venv).
- **Linter/Formatter**: `ruff` (configuration in `pyproject.toml`).

## Dependency Management
- **Add Dependency**: `uv add [package]`
- **Add Dev Dependency**: `uv add --dev [package]`
- **Install/Sync**: `uv sync`

## Code Quality
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .` (or `uv run black .` if preferred, but ruff is default).
    - Note: User preferences mention `black`, but `ruff` is configured in `pyproject.toml`. Follow `pyproject.toml` or user preference for `black`.

## Build System
- **Backend**: `setuptools.build_meta`
