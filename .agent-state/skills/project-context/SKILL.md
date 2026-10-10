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
2. **Contextualize**: Understand the `source → transform → render → verify` pipeline.
3. **Persist**: Keep `.ai-context` files updated.

## Instructions and Rules

### 1. Core Purpose
- `ai-context-core` is a **context compiler** for AI-assisted coding (`source → transform → render → verify`).
- Produces token-efficient, versioned, verifiable context artifacts; consumes analysis from `qgis-plugin-analyzer` (the builtin source is a standalone fallback).

### 2. Project Structure
- `src/ai_context_core`: Main package source.
- `docs/`: Technical documentation.
- `.agent/`: Agentic framework (git submodule — `agentic-forge`).
- `.agent-state/`: Project-owned state (memory, task, overlay skills).
- `pyproject.toml`: Global config and dependencies (uv).

### 3. Architecture (Pipeline)
- Context compiler: `sources → context → render → verify`.
- Builtin source: engine → providers → visitors/builders → reporting; one AST visitor per concern, no I/O inside visitors.

### 4. Critical Commands
- `ai-ctx context`: Primary path — render `AI_CONTEXT.md` + context artifacts.
- `ai-ctx verify`: Exit 1 when artifacts are stale vs. sources.
- `ai-ctx health`: Freshness, tokens, symbols, provenance.
- `ai-ctx stats`: Quick project statistics.

## Quality Checklist
- [ ] Is the engine→reporting pipeline mentioned?
- [ ] Is the structure description accurate?
- [ ] Are the terminal commands correct?
- [ ] Are workspace paths referenced correctly?
