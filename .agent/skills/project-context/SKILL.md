---
name: project-context
description: Core knowledge about ai-context-core project
trigger: context, overview, about, project structure
---

# Project Context: ai-context-core

## Overview
`ai-context-core` is the central nervous system for AI-assisted coding workflows.
It provides AST analysis, context management, and profile-based rules (e.g., for QGIS plugins).

## Key Features
- **Project Analysis**: Deep AST analysis for Python projects.
- **Context Management**: Keeps `.ai-context` files updated.
- **Profiles**:
    - `python-generic`: Standard Python support.
    - `qgis-plugin`: Specialized rules for QGIS plugin development.

## Project Structure
- `src/ai_context_core`: Main package source.
- `docs/`: Documentation.
- `.agent/`: Agentic framework configuration.
- `pyproject.toml`: Configuration and dependencies (managed by `uv`).

## Commands
- `ai-ctx init --profile [profile]`: Initialize new project.
- `ai-ctx analyze`: Update context manually.
