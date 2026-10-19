# qgis-plugin-manager — Agentic Forge v1.4.1 Reconciliation

- **Date**: 2026-10-18
- **Target**: `qgis-plugin-manager` `.agent` submodule
- **Current pin**: `v1.2.0` (`2de22cf`) with a large local framework fork
- **Target pin**: `v1.4.1` (`537f9fd`)
- **Status**: ⚠️ Manual reconciliation required; the deployment helper correctly
  refuses the dirty worktree.

## Findings

`qgis-plugin-manager` has **34 changed/untracked framework paths** in `.agent`
(25 modified + 9 untracked). Every one of those paths has a counterpart in
`agentic-forge` v1.4.1; the tooling, tests, requirements, workflows and generic
docs were upstreamed or superseded:

| Category | Local paths | v1.4.1 equivalent |
| :--- | :--- | :--- |
| Tooling | `tools/forge.py`, `forge_metrics*.py`, `forge_paths.py`, `lesson_extractor.py`, `memory_prune.py`, `validate_agent_system.py` + untracked `agent_links.py`, `frontmatter.py`, `project_commands.py`, `skill_conflicts.py`, `workflow_graph.py` | Included, plus `--version`, `tomli` fallback, project commands and config keys |
| Tests | `tests/` (untracked) | Included; 33 tests |
| Runtime deps | `requirements.txt` (untracked) | Included (`PyYAML`, conditional `tomli`) |
| Workflows | 13 modified workflow files | Included; use `forge.py project` and `testing-standards` |
| Generic docs | `AGENTS.md`, `README.md`, `QUICK_REFERENCE.md` | Genericized, no consumer-specific names |
| Domain pack | 3 QGIS workflow templates | Included with `template: true` and validated refs |
| Skills | `coding-standards`, `documentation-standards` | Included with project `max_cc` and generic log paths |

The parent repository's own `scaffold/qgis/skills/qa-docker/SKILL.md` is **not**
inside `.agent`; it is project-owned and is not touched by this reconciliation.
v1.4.1 also keeps a deprecated core `qa-docker` alias for existing overlays.

## Recommended procedure

1. **Save the parent worktree** (the helper requires a clean repository):
   ```bash
   cd ~/qgispluginsdev/qgis-plugin-manager
   git status
   git add -A && git commit -m "wip: save qgis-plugin-manager work"   # or git stash
   ```
2. **Back up the local framework fork**:
   ```bash
   git -C .agent diff > /tmp/qgis-plugin-manager-agent-local.patch
   git -C .agent status --short >> /tmp/qgis-plugin-manager-agent-local.patch
   ```
3. **Review the backup** and keep anything project-specific. The categories above
   are superseded by v1.4.1; do not blindly keep a second copy of the tooling.
4. **Clean the submodule** (only after the backup):
   ```bash
   git -C .agent checkout -- .
   git -C .agent clean -fd
   ```
5. **Deploy v1.4.1** with the helper:
   ```bash
   cd ~/qgispluginsdev/ai-context-core
   ./scripts/deploy_agentic_forge.sh ~/qgispluginsdev/qgis-plugin-manager
   ./scripts/deploy_agentic_forge.sh ~/qgispluginsdev/qgis-plugin-manager --apply
   ```
6. **Run the project CI checks**:
   ```bash
   cd ~/qgispluginsdev/qgis-plugin-manager
   uv pip install -r .agent/requirements.txt
   uv run ruff check .agent/tools .agent/tests
   uv run ruff format --check .agent/tools .agent/tests
   uv run mypy .agent/tools .agent/tests
   uv run pytest .agent/tests -q
   uv run python .agent/tools/forge.py validate
   uv run python .agent/tools/forge.py metrics validate
   ```

## Rollback

```bash
git -C .agent checkout v1.2.0
git -C .agent apply /tmp/qgis-plugin-manager-agent-local.patch
git add .agent
git commit -m "chore(agent): restore local framework fork"
```

## Why not discard automatically

The local fork contains consumer-specific docs and QGIS workflow templates. The
tooling/tests/requirements portions are safe to replace with v1.4.1, but the
domain-pack and documentation portions should be reviewed, not overwritten
blindly. That is why the helper refuses dirty trees and this reconciliation is
manual.
