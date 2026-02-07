
# Quick Start Guide

Follow these steps to set up `ai-context-core` as a standalone repository.

## 1. Move and Isolate
Move the folder to your projects directory (outside the current project).

```bash
# Example: move to your projects folder
mv migration/ai-context-core ~/projects/ai-context-core
cd ~/projects/ai-context-core
```

## 2. Initialize Git
Set up version control for the new repository.

```bash
git init
# Create basic .gitignore if it doesn't exist
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo ".ai-context/" >> .gitignore
echo "dist/" >> .gitignore
echo "analysis_results/" >> .gitignore

git add .
git commit -m "feat: initial commit of ai-context-core structure"
```

## 3. Install Dependencies
Use `uv` to create the virtual environment and install the package in editable mode.

```bash
# Create venv and install dependencies defined in pyproject.toml
uv venv
uv sync
```
*Note: If you prefer standard pip: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`*

## 4. Verification (Health Check)
Verify that the CLI is installed and your environment is ready using the `doctor` command.

```bash
# Checks requirements, project structure, and config health
uv run ai-ctx doctor
```

## 5. First Run ("Interactive Mode")
The easiest way to start is using the **Interactive Mode**, which will guide you through initialization and analysis.

```bash
uv run ai-ctx interactive
```

*Prefer the manual way?*
1. **Initialize**: `uv run ai-ctx init --profile generic`
2. **Analyze**: `uv run ai-ctx analyze`

## 🚀 Next Steps: Explore the Suite
Once initialized, try these commands to understand your codebase better:
- **`ai-ctx graph`**: Generate an architectural dependency diagram.
- **`ai-ctx roadmap`**: Identify which files to refactor first.
- **`ai-ctx audit`**: Check the absolute Quality Score of your project.

---
*Note: Thanks to the **Incremental Cache**, subsequent analysis runs will be near-instant!*
