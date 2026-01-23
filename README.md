# AI Context Core

The central nervous system for your AI-assisted coding workflow.

## Features
- **Project Analysis**: Deep AST analysis for Python projects.
- **Context Management**: Keeps `.ai-context` files updated.
- **Profiles**: 
    - `python-generic`: Standard Python support.
    - `qgis-plugin`: Specialized rules for QGIS plugin development.
- **Workflow Automation**: Standardized scripts for session management.

## Installation

### Globally (as a tool)

```bash
uv tool install .
```

### In a Virtual Environment (Recommended for development)

1. **Create and activate the environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install the package (editable)**:
   ```bash
   uv sync
   ```

This will install the project and its dependencies in the `.venv` directory. The `ai-ctx` command will be available within the virtual environment.

### Using in Another Project

If you want to use `ai-ctx` within the context of **another project's** virtual environment:

#### Option A: One-off execution (No installation required)
You can run it directly using the path to this repository:
```bash
uv run --with /path/to/ai-context-core ai-ctx analyze
```

#### Option B: Install in an existing environment
Activate your project's environment and run:
```bash
uv pip install /path/to/ai-context-core
```

#### Option C: Add as a development dependency
If the other project also uses `uv`:
```bash
uv add --dev --path /path/to/ai-context-core
```

## Usage

```bash
# Initialize in a new project
ai-ctx init --profile qgis-plugin

# Update context manually
ai-ctx analyze
```
