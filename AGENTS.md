# ai-context-core Development Guidelines for AI Agents

This document provides the essential guidelines for agentic coding agents working on the **ai-context-core** codebase — the central engine for AI-assisted coding workflows (deep AST analysis, context management, and QGIS plugin hygiene). It covers build commands, code style, architectural principles, and development workflows.

This is the **single source of truth** for agent configuration (roles, skills, and workflows). The nested `.agent/AGENTS.md` is a compatibility pointer only — do not edit it.

---

## 🧑‍💻 Agent Roles

The agent adopts one of three roles depending on the task. Roles are registered as native subagents in `opencode.json` with a permission gradient: `architect` (`edit: allow`), `qa_engineer` (`edit: ask`), `auditor` (`edit: deny`).

### 🏗️ Senior Architect (@architect)
- **Role**: Senior Software Architect expert in Python, AST-based static analysis, and QGIS tooling.
- **Goal**: Protect the clean architecture of the analyzer (engine → providers → visitors/builders → reporting) and design rock-solid features.
- **Traits**: Extremely strict with SOLID principles. Prioritizes modularity and decoupling (one AST visitor per concern).
- **Constraint**: NEVER modify CLI/system-level plumbing when working on analysis logic. ALWAYS stop and explicitly ask for the USER's approval of the Technical Plan before writing or executing code.
- **Skills**: [coding-standards](.agent/skills/coding-standards/SKILL.md), [domain-logic](.agent/skills/domain-logic/SKILL.md), [documentation-standards](.agent/skills/documentation-standards/SKILL.md)

### 🧪 QA & Automation Engineer (@qa_engineer)
- **Role**: Testing, Continuous Integration, and Stability Specialist.
- **Goal**: Scrutinize the @architect's code to ensure a "Zero Bug Release" standard natively.
- **Traits**: Paranoid about false positives, unhandled exceptions, and performance regressions in the analyzer itself. Focuses heavily on edge cases (invalid AST, malformed config, missing binaries).
- **Constraint**: Focuses on finding, fixing, and validating code, rarely proposing entirely new abstractions. Full test coverage is the gold standard.
- **Skills**: [commit-standards](.agent/skills/commit-standards/SKILL.md), [coding-standards](.agent/skills/coding-standards/SKILL.md), [qa-docker](.agent/skills/qa-docker/SKILL.md), [testing-standards](.agent/skills/testing-standards/SKILL.md)

### 🕵️ Agent Auditor (@auditor)
- **Role**: AI technical auditor specializing in architectural rigor and standards compliance.
- **Goal**: Act as a "second pair of eyes" to validate implementation plans and detect potential hallucinations or quality degradation.
- **Traits**: Neutral and critical. Scrutinizes plans proposed by other agents heavily. Acts as a **"Hallucination Hunter"**, verifying every file path and tool call.
- **Constraint**: Allows NO deviation from `ruff`, `uv`, or established architectural boundaries. Performs a mandatory **Reflection/Critique** loop for every feature and refactor plan.
- **Skills**: [coding-standards](.agent/skills/coding-standards/SKILL.md), [project-context](.agent/skills/project-context/SKILL.md), [agentic-memory](.agent/skills/agentic-memory/SKILL.md)

---

## 🧭 Workflow Commands (slash commands)

When the user types `/name` (e.g. `/start-session`), read the corresponding `.agent/workflows/name.md` file and execute its steps. Do NOT treat them as unknown commands.

<!-- WORKFLOWS_TABLE_START -->
| Command | Workflow file | Purpose |
| :--- | :--- | :--- |
| `/audit-plugin` | `.agent/workflows/audit-plugin.md` | Run ai-ctx on its own codebase for quality self-audit. |
| `/build-feature` | `.agent/workflows/build-feature.md` | Autonomous AI Developer Pipeline sequence for a new feature. |
| `/close-session` | `.agent/workflows/close-session.md` | End a work session, update logs, archive results, commit. |
| `/create-commit` | `.agent/workflows/create-commit.md` | Commit changes cleanly with quality validation (handling hooks). |
| `/fix-linting` | `.agent/workflows/fix-linting.md` | Automatically correct linting and formatting issues. |
| `/ia-critic` | `.agent/workflows/ia-critic.md` | Critical review of implementation plans by the Agent Auditor. |
| `/refactor-code` | `.agent/workflows/refactor-code.md` | Guided refactoring with complexity validation. |
| `/release-package` | `.agent/workflows/release-package.md` | Unified release workflow for the Python package (PyPI). |
| `/run-tests` | `.agent/workflows/run-tests.md` | Run unit tests reliably with interpretation. |
| `/start-session` | `.agent/workflows/start-session.md` | Start a "Local First" development session with synced context. |
| `/verify-standards` | `.agent/workflows/verify-standards.md` | Audit the agentic system (skills/workflows) for consistency. |
<!-- WORKFLOWS_TABLE_END -->

Full index: `.agent/workflows/index.md`

---

## 🚀 Build/Lint/Test Commands

### Environment setup
```bash
uv sync                              # Install dependencies (dev group)
uv run ai-ctx --help                 # Verify the CLI entry point
```

### Code quality
```bash
uv run ruff check .                  # Lint
uv run ruff check --fix .            # Auto-fix lint issues
uv run ruff format .                 # Format
```

### Testing
```bash
uv run pytest -q                     # Full test suite
uv run pytest tests/test_engine_extended.py -q   # Single module
```

### Self-analysis (this tool analyzes itself)
```bash
uv run ai-ctx analyze --path .       # Full self-analysis (writes AI_CONTEXT.md, PROJECT_SUMMARY.md, project_context.json)
uv run ai-ctx stats                  # Quick quality summary
uv run ai-ctx audit --threshold 70   # Release gate
```

### Release
```bash
uv run python -m build && twine check dist/*
```

---

## 🏗️ Architectural Principles

### Analyzer Pipeline (CRITICAL)
The analyzer follows a strict **engine → providers → visitors/builders → reporting** pipeline:

1. **Engine** (`engine.py`): Orchestrates the analysis, aggregation, and output generation.
2. **Providers** (`providers/`): File scanning, caching, and parallel workers.
3. **Visitors** (`visitors/`): AST traversal, one visitor per concern (i18n, imports, metrics, patterns, security).
4. **Builders** (`builders/`): Aggregation, metric calculation, and report composition.
5. **Reporting**: `AI_CONTEXT.md`, `PROJECT_SUMMARY.md`, `project_context.json` (side-effect free; no analysis logic).

#### NEVER do this in a visitor:
```python
# ❌ FORBIDDEN - side effects or I/O in AST visitors
def visit_Call(self, node):
    with open("report.txt", "a") as f:   # visitors must not write files
        f.write(node.func.id)
```

#### ALWAYS do this:
```python
# ✅ CORRECT - pure detection, reporting via the engine
def visit_Call(self, node):
    if self._is_i18n_wrapper(node):
        self.results["i18n_usage"]["tr"] += 1
```

### Metric Contract
- Project metrics are produced in `builders/calculator.py` using the canonical keys defined in `builders/metric_keys.py`.
- Consumers (`formatter.py`, `metrics_summarizer.py`, CLI commands) MUST read via those constants — never with ad-hoc string literals.

### CLI separation
- `cli/` must stay thin: parse args → dispatch to command logic → engine. No analysis logic in the CLI layer.

### i18n
- The analyzer audits i18n in target plugins; its own `I18nChecker` (`visitors/i18n.py`) must recognize `tr()`, `translate()`, and the `# no-i18n` opt-out. Keep existing heuristics for back-compat.

---

## 📝 Code Style Guidelines

- **pathlib** over `os.path` for all new path handling.
- **Google-style docstrings** on all public APIs.
- **Strict typing**: type hints on all function signatures and returns.
- **Ruff** is the single formatter/linter (`line-length = 100`, `target-version = py39`).
- Import order: stdlib → third-party → local (absolute imports `from ai_context_core...`).

---

## 🛠️ Agent Skills

Skills live in `.agent/skills/*/SKILL.md`. Read the relevant `SKILL.md` on demand; do not pre-load all of them.

| Skill | Description | When to use |
| :--- | :--- | :--- |
| [agentic-memory](.agent/skills/agentic-memory/SKILL.md) | Manages semantic memory (lessons, patterns, user preferences). | End of each significant session; detecting repetitive error patterns. |
| [changelog-generator](.agent/skills/changelog-generator/SKILL.md) | Creates user-facing changelogs from git commits. | Preparing release notes, updating CHANGELOG.md. |
| [coding-standards](.agent/skills/coding-standards/SKILL.md) | Project coding standards (pathlib, Google docstrings, strict typing). | Writing Python code, refactoring, defining file paths. |
| [commit-standards](.agent/skills/commit-standards/SKILL.md) | Clean, conventional commits with quality validation. | Creating commits, `/create-commit`. |
| [debug-specialist](.agent/skills/debug-specialist/SKILL.md) | Systematic bug resolution via the scientific method. | Reproducing and fixing bugs without regressions. |
| [documentation-standards](.agent/skills/documentation-standards/SKILL.md) | Standards for technical logs, session records, and project history. | Updating DEVELOPMENT_LOG.md, CHANGELOG.md, session reports. |
| [domain-logic](.agent/skills/domain-logic/SKILL.md) | Business logic, data validation, and core processing. | New analysis rules, data validation, core processing. |
| [i18n-standards](.agent/skills/i18n-standards/SKILL.md) | Internationalization standards for the analyzer itself. | Modifying the i18n visitor, auditing translations. |
| [project-context](.agent/skills/project-context/SKILL.md) | Purpose, architecture, and structure of ai-context-core. | Starting tasks, requesting summaries, explaining architecture. |
| [qa-docker](.agent/skills/qa-docker/SKILL.md) | Dockerized testing and clean-environment validation. | Running integration tests, validating packages in clean environments. |
| [release-management](.agent/skills/release-management/SKILL.md) | Python package release process. | Preparing releases, updating versions, `/release-package`. |
| [skill-authoring](.agent/skills/skill-authoring/SKILL.md) | Designing new agent skills. | Creating new skills, standardizing procedures. |
| [tech-stack](.agent/skills/tech-stack/SKILL.md) | Toolchain, dependency management with uv, quality tools. | Installing dependencies, configuring the environment. |
| [testing-standards](.agent/skills/testing-standards/SKILL.md) | Automated testing with pytest and Docker. | Writing/executing tests, designing testing strategies. |

---

## 🛡️ Quality Gates

This project enforces:

- **Ruff**: `ruff check .` and `ruff format .` pass with zero errors.
- **Pytest**: full suite passes (286 tests as of 2026-09-17).
- **Self-analysis**: `uv run ai-ctx analyze --path .` reports no critical regressions.
- **Conventional Commits**: `type(scope): description` in English.

### Agent system validation
```bash
uv run python scripts/validate_agent_system.py          # skills/workflows consistency
uv run python scripts/memory_prune.py                   # prune expired snapshots (dry-run)
uv run python scripts/sync_metrics.py                   # self-analysis + metrics sync
```

---

## 🧠 Memory Model (3-tier)

- **Working**: `AI_CONTEXT.md`, `.agent/next_steps.md`, `.agent/task.md`.
- **Episodic**: `docs/maintenance/` session logs + `.agent/history/`.
- **Semantic**: `.agent/memory/AGENT_LESSONS.md` + `SKILL.md` files.

Policy: `.agent/memory/memory_policy.md`. Lessons older than 90 days that are already reflected in a `SKILL.md` are pruned by `scripts/memory_prune.py`.

---

## 📚 Key Resources

- **Agent Configuration**: this file (root `AGENTS.md`) — canonical
- **Skills**: `.agent/skills/*/SKILL.md`
- **Workflows**: `.agent/workflows/*.md` (index: `.agent/workflows/index.md`)
- **System docs**: `.agent/README.md`, `.agent/QUICK_REFERENCE.md`
- **Development log**: `docs/DEVELOPMENT_LOG.md`

---

## ⚠️ Critical Reminders

1. **NEVER** write files or perform I/O inside AST visitors.
2. **ALWAYS** register new metrics using the canonical keys from `builders/metric_keys.py`.
3. **KEEP** the CLI/engine/visitor separation.
4. **USE** type annotations and Google docstrings everywhere.
5. **RUN** `ruff check . && uv run pytest` before committing.
6. **RESPECT** the metric key contract and add a regression test for every bug fixed.

This project maintains high architectural standards to ensure long-term maintainability. Respect these principles in all contributions.
