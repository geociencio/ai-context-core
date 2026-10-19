# Agentic Forge v1.3.0 — P0 Quality-Gate Fixes (Cross-Repo Proposal)

- **Date**: 2026-10-18
- **Framework**: `agentic-forge` (`.agent/` submodule)
- **Base**: `v1.2.0` (`2de22cf`, detached)
- **Proposed branch**: `fix/p0-quality-gates`
- **Local commits**: `d240b54` — `fix: enforce validation and memory gates (v1.3.0)`,
  `8967cb6` — `docs: keep memory prune wording generic`
- **Parent pin**: intentionally **unchanged** (`v1.2.0`) until the framework commit
  is pushed and tagged.

## Why this document exists

`agentic-forge` is mounted as a git submodule and shared by sibling repositories.
Framework changes therefore must be **generic**, **backward compatible** and
released through the framework repository, not committed only inside one consumer.
This document records the changes, their compatibility impact and the rollout
steps for every sibling repo.

## Changes in v1.3.0

| Area | Change | Compatibility |
| :--- | :--- | :--- |
| `validate --graph` | Exits `1` when a workflow references an unknown skill or script (previously always `0` unless `--validate`/`--json`). | Bug fix. Repos with broken references will now fail; that is the documented contract. |
| `metrics validate` | Excludes `scaffold/<domain>/` from project-ground-truth checks. | Generic; removes domain-pack false positives. |
| `coding-standards` | References `[project].max_cc` (default `10`) instead of hardcoding CC 10. | Backward compatible: projects without `max_cc` keep the old default. |
| `memory prune` | Parses Markdown-bullet lessons, still supports fenced YAML (rewritten under `--apply`), lazy PyYAML import, non-zero exit on parse errors. | Broadens support; no project-specific assumptions. |
| `memory prune` default | Dry-run by default; `--apply` required to rewrite/delete. | **Behavior change**: custom close-session flows must add `--apply`. |
| Docs | `README`, `QUICK_REFERENCE`, `workflows/index.md`, `close-session.md` updated; `CHANGELOG.md` added. | Documentation only. |

## Migration for sibling repositories

1. **Close-session flows**: if a project keeps its own workflow that calls
   `forge.py memory prune` expecting deletion, change it to
   `forge.py memory prune --apply`. Add `--apply` only after reviewing the
   dry-run output.
2. **Broken references**: run `python .agent/tools/forge.py validate --graph`
   before updating. Repositories with broken skill/script references must fix
   them; `--graph --json` prints the machine-readable report.
3. **Complexity limits**: projects that relied on the hardcoded CC 10 should set
   `[project].max_cc` in `forge.toml` to their real limit. Without it, the
   default remains 10.
4. **YAML lessons**: files with a fenced ```yaml block continue to work and are
   rewritten by `--apply`; no migration is required.
5. **No changes to project state**: `.agent-state/` layout, metrics schema and
   skill overlay are untouched by the framework update.

## Rollout checklist

- [ ] Push `fix/p0-quality-gates` to `codeberg.org/geociencio/agentic-forge`.
- [ ] Open a PR; review the `CHANGELOG.md` compatibility notes.
- [ ] Merge and tag `v1.3.0`.
- [ ] In each sibling repo:
  ```bash
  git -C .agent fetch --tags
  git -C .agent checkout v1.3.0
  git add .agent
  git commit -m "chore(agent): bump agentic-forge to v1.3.0"
  ```
- [ ] Run the framework gates in each repo:
  ```bash
  python .agent/tools/forge.py validate
  python .agent/tools/forge.py validate --graph
  python .agent/tools/forge.py validate --conflicts
  python .agent/tools/forge.py metrics validate
  python .agent/tools/forge.py memory prune
  ```
- [ ] Update any custom workflow that expected automatic pruning to pass
  `--apply`.

## Verification performed in this repository

| Check | Result |
| :--- | :--- |
| `forge.py validate` | exit 0 (15 skills, 14 workflows) |
| `forge.py validate --graph` | exit 0 with valid refs; exit 1 with a deliberately broken workflow |
| `forge.py validate --conflicts` | exit 0 |
| `forge.py metrics validate` | exit 0 (was 5 violations / exit 1) |
| `forge.py memory prune` | exit 0, dry-run on bullet lessons |
| `forge.py memory prune --apply` | YAML fixture rewritten correctly; old consolidated lesson moved to `[PRUNED]` |
| Sibling simulation | `max_cc = 15`, `scaffold/demo`, bullet lessons and a valid `scripts/` reference: `validate`, `--graph`, `--conflicts`, `metrics validate` and dry-run/`--apply` all green |

## Rollback

Keep the parent gitlink at `v1.2.0` until `v1.3.0` is tagged. To roll back a
consumer that already updated:

```bash
git -C .agent checkout v1.2.0
git add .agent
git commit -m "chore(agent): roll back agentic-forge to v1.2.0"
```
