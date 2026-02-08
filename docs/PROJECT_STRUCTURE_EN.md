# AI-Context-Core - Project Structure

## Project Overview

**AI-Context-Core** is a high-performance, AI-native context extraction and analysis tool designed to build rich knowledge bases for LLMs from source code. It specializes in extracting architectural patterns, dependency graphs, security hot-spots, and quality metrics using advanced AST (Abstract Syntax Tree) analysis.

**Version**: 3.2.0
**Author**: Juan M Bernales
**License**: GNU General Public License v3 (GPLv3)
**Repository**: https://github.com/geociencio/ai-context-core

## Technology Stack

### Runtime Environment
- **Python**: 3.10+ (Fully compatible with Python 3.14)
- **Dependency Manager**: `uv` (Fastest Python package installer and resolver)
- **Core Libraries**: `ast`, `pathlib`, `json`, `jinja2`

### Development & Quality Tools
- **Static Analysis**: `ruff` (Fast linting and formatting)
- **Formating**: `black`
- **Testing**: `pytest`
- **Metrics**: `ai-ctx analyze` (Self-analyzing project)
- **Agentic Infrastructure**: Antigravity Framework (Automated workflows and skills)

## Directory Structure

```text
ai-context-core/
├── 📁 .agent/                  # Agentic Intelligence Layer
│   ├── 📁 skills/              # Specialized agent capabilities
│   └── 📁 workflows/           # Automated development pipelines
│
├── 📁 docs/                    # Technical Documentation
│   ├── COMMIT_GUIDELINES.md    # Standard for git commits
│   └── PROJECT_STRUCTURE_EN.md ⭐ (This document)
│
├── 📁 src/                     # Source Code
│   └── 📁 ai_context_core/     # Main Package
│       ├── 📁 analyzer/        ⭐ Core Analysis Engine (Modular)
│       │   ├── 📁 visitors/    # AST Analyzers (Issues, Patterns, Complexity)
│       │   ├── 📁 builders/    # Report & Data Construction (HTML, Markdown)
│       │   ├── 📁 providers/   # Data Sources (FS, Git, QGIS)
│       │   ├── 📁 context_builders/ # Knowledge base generation
│       │   └── engine.py       # Main Orchestration Logic
│       │
│       ├── 📁 cli/             # CLI Implementation
│       │   ├── 📁 commands/    # ActionHandlers (audit, analyze, qgis)
│       │   └── __init__.py     # Click CLI entry point
│       │
│       ├── 📁 config/          # Configuration System (Profiles, Defaults - TOML)
│       └── 📁 context/         # Semantic Memory & Context Storage
│
├── 📁 tests/                   # Comprehensive Test Suite
│   ├── conftest.py             # Global fixtures
│   └── test_*.py               # Automated unit and integration tests
│
├── 📄 pyproject.toml           # Project metadata & dependencies
├── 📄 Makefile                 # Task automation (shortcuts)
├── 📄 README.md                # Gateway documentation
└── 📄 uv.lock                  # Deterministic dependency lock
```

## Key Components Description

### Analysis Engine (`src/ai_context_core/analyzer/`)

- **`visitors/`**: Modules that traverse the Abstract Syntax Tree (AST) to detect code smells, design patterns (Singleton, Strategy, etc.), and potential security vulnerabilities.
- **`builders/`**: Responsible for aggregating raw analysis data into structured reports (HTML, JSON, Markdown) and calculating complex metrics like the Maintenance Index.
- **`providers/`**: Adapters that interface with the environment, such as reading from the filesystem, analyzing Git history for hotspots, or extracting QGIS-specific metadata.
- **`engine.py`**: The central controller that manages the analysis pipeline, parallelizing tasks across multiple workers for maximum speed.

### CLI Layer (`src/ai_context_core/cli/`)

The CLI follows the **Command Pattern**. Each high-level action (`analyze`, `audit`, `qgis`, `context`) is implemented as an independent handler, allowing for easy extensibility and testing.

### Context System (`src/ai_context_core/context/`)

Manages the persistent "Project Brain". It stores semantic metadata and serialized project states in `project_context.json`, which agents use to understand the codebase without re-analyzing everything.

### Agentic Layer (`.agent/`)

Integrating the **Antigravity Framework**, this project is managed by an autonomous agentic system.
- **Workflows**: Scripts that automate complex tasks like releases (`/release-package`) or session cleanup (`/cierra-sesion`).
- **Skills**: Domain-specific knowledge that agents use to ensure coding standards, handle project context, or debug issues.

## Developer Workflow

### Environment Setup
```bash
# Install dependencies with uv
uv sync
```

### Common Commands
- **Run Quality Audit**: `uv run ai-ctx audit`
- **Full Project Analysis**: `uv run ai-ctx analyze --path .`
- **Run Tests**: `uv run pytest`
- **Format Code**: `uv run black .`

## Architecture Principles

1.  **Immutability**: Context snapshots are preserved to allow temporal reasoning.
2.  **Modularity**: Decoupled `visitors` and `builders` allow adding new analysis rules without touching the core engine.
3.  **AST-First**: Heavy reliance on static analysis for language-agnostic precision.
4.  **Agent-Native**: Designed to be read and modified by both humans and AI agents.
