---
name: project-context
description: Purpose, architecture, and structure of ai-context-core.
trigger: when starting tasks, requesting summaries, or explaining the architecture.
---

# Project Context

Defines the core knowledge about `ai-context-core`: its architecture, key components, and operational flow.

## When to use this skill
- When starting a session on the project.
- When explaining the architecture to a new contributor (human or AI).
- When unsure about file locations or module responsibilities.
- To orient development toward the project goals.

## Degree of Freedom
- **Guided**: Project structure and commands are fixed; flow interpretation is open.

## Workflow
1. **Identify**: Locate main components (`src`, `docs`, `.agent`).
2. **Contextualize**: Understand the AST analysis ↔ profile relationship.
3. **Persist**: Keep `.ai-context` files updated.

## Instructions and Rules

### 1. Core Purpose
- `ai-context-core` is the central engine for AI-assisted coding workflows.
- Provides deep AST analysis and profile-based context management (generic Python, QGIS plugins).

### 2. Project Structure
- `src/ai_context_core`: Main package source.
- `docs/`: Technical documentation.
- `.agent/`: Agentic framework configuration (skills, workflows, memory).
- `pyproject.toml`: Global config and dependencies (uv).

### 3. Architecture (Pipeline)
- engine → providers → visitors/builders → reporting.
- One AST visitor per concern; no I/O inside visitors.

### 4. Critical Commands
- `ai-ctx analyze`: Run analysis and regenerate context files.
- `ai-ctx stats`: Quick quality summary.
- `ai-ctx audit --threshold N`: CI/CD release gate.

## Quality Checklist
- [ ] Is the engine→reporting pipeline mentioned?
- [ ] Is the structure description accurate?
- [ ] Are the terminal commands correct?
- [ ] Are workspace paths referenced correctly?
