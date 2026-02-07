# Agentic Systems Implementation Guide (Antigravity)

This guide explains how to port the intelligence infrastructure (Skills, Workflows, and Roles) from this project to any other Python repository or QGIS Plugin to maximize productivity with AI.

## 1. Prerequisites

- **Antigravity CLI**: Installed and configured in your environment.
- **Access to Gemini (or compatible LLM)**: With read/write permissions in the workspace.
- **Base Structure**: The project must have a `pyproject.toml` file (preferably managed with `uv`).

## 2. Initializing the `.agent` Folder

The "brain" of the agent lives in the `.agent/` folder. Create it in the root of your new project:

```bash
mkdir -p .agent/{skills,workflows,memory,resources}
```

### Master File: `AGENTS.md`
Create the `.agent/AGENTS.md` file defining the roles. You can copy the structure from this project:

```markdown
# AI Agents & Roles
## Main Profiles
### 🧠 Senior Architect
**Focus**: System Design and Core Logic.
...
```

## 3. Implementing Skills

Copy the essential skills from this project to your new `.agent/skills/` folder. The "must-haves" are:

1.  **coding-standards**: Defines how you want the AI to write code (e.g., using `pathlib`).
2.  **commit-standards**: Ensures that the Git history is readable.
3.  **project-context**: Helps the AI not to "hallucinate" about the architecture.
4.  **creador-de-skills-antigravity**: The tool for the AI itself to expand its capabilities.

*Important: Adjust the rules in `coding-standards` if your new project uses different standards (e.g., Django vs. Flask).*

## 4. Setting Up Workflows

Workflows allow you to automate multi-stage processes. The recommended minimums in `.agent/workflows/` are:

- **inicia-sesion.md**: Synchronizes context and verifies the environment.
- **cierra-sesion.md**: Documents progress and ensures persistence.
- **run-tests.md**: Automates quality verification.

## 5. Differences by Project Type

### Standard Python Project
- **Tech Stack Focus**: Ensure the `tech-stack` skill reflects your package manager (uv, poetry, pip).
- **Tests Focus**: Configure `run-tests.md` for your framework (pytest, nose, unittest).

### QGIS Plugin
- **Resources**: It is vital to include a **QGIS Mocking Guide** in `.agent/resources/` so the AI can test without the QGIS binary.
- **Validation**: Add a release workflow (`release-package.md`) that verifies the `metadata.txt` file and packages the ZIP correctly.
- **Roles**: Activate the **GIS-Architect** role to specifically handle spatial logic and PyQt.

## 6. Best Practices for Success

1.  **Persistent Memory**: Always keep a `.agent/memory/AGENT_LESSONS.md` file updated. This is where the AI stores your design quirks and preferences "outside the manual."
2.  **Auditability**: Use the `verificar-estandares.md` workflow once a week to ensure the system doesn't degrade.
3.  **Language**: Keep the agent documentation in a single language (preferably **English**) to avoid token confusion and maintain consistency with international standards.

---
*Manual generated for: Antigravity Ecosystem*
*Version: 1.2*
