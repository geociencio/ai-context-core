# Agentic Forge v1.4.0/v1.4.1 — Hardening Completion

- **Date**: 2026-10-18
- **Framework**: `agentic-forge` v1.4.0 (hardening) + v1.4.1 (compatibility)
- **Commit / tag**: `5f9c665` / `v1.4.0`; `537f9fd` / `v1.4.1`
  (published to `codeberg.org/geociencio/agentic-forge`)
- **Supersedes**: the v1.3.0 P0 proposal in
  [`agentic_forge_p0_quality_gates.md`](agentic_forge_p0_quality_gates.md)
- **Status**: ✅ Released; `sec_interp` passes the v1.4.1 simulation and is
  ready for the deployment helper.

## v1.4.1 compatibility patch

v1.4.0 removed `qa-docker`, but existing project overlays and `AGENTS.md` links
still reference it. v1.4.1 restores it as a **deprecated, pointer-only alias** for
`testing-standards`, so v1.3.x consumers keep validating without duplicated
guidance. The alias is scheduled for removal in the next major release.

## Checklist from the v1.3.0 review

| Pending item | Status | Evidence |
| :--- | :--- | :--- |
| 0 tests / 0 CI | ✅ Fixed | 32 pytest tests in `.agent/tests/`; `.github/workflows/ci.yml`, `.forgejo/workflows/ci.yml` and `scripts/ci.sh`; CI runs Ruff, format, mypy, pytest, validation and memory check. |
| 17 Ruff findings | ✅ Fixed | Ruff 0.17.1 clean over `tools/` and `tests/`; explicit rule selection in `ruff.toml`. |
| 5 mypy errors | ✅ Fixed | `mypy` clean over 19 files (`mypy.ini`, `types-PyYAML`, `tomli`; `mypy>=1.10,<2`). |
| 4 unformatted files | ✅ Fixed | `ruff format --check` reports 19 files already formatted. |
| Scaffold unvalidated | ✅ Fixed | Domain-pack skills/workflows are validated (17 skills, 14 workflows, 3 templates); `audit-plugin` now uses `qgis-core`; all templates carry `template: true`. |
| Genericization incomplete | ✅ Fixed | Core tooling/docs no longer reference `qgis_analyzer`, `qgis-analyzer`, `SecInterp`, `docs/source/` or `763`; a regression test enforces the ban. Domain packs remain intentionally QGIS-specific. |
| Config keys ignored | ✅ Fixed | `test_command`, `test_command_full`, `lint_command`, `format_command`, `version_bump_command`, `strict_agent_system` and `max_lesson_lines` are read from `forge.toml`; `forge.py project` runs them. |
| No `--version` | ✅ Fixed | `forge.py --version` reads `.agent/VERSION` (`1.4.0`). |
| Python 3.11+ vs project >=3.9 | ✅ Fixed | `tomli` fallback for < 3.11, `timezone.utc` instead of `datetime.UTC`, `requirements.txt`, and a Python 3.9 CI job. |
| 7/14 workflow skill mismatches | ✅ Fixed | `QUICK_REFERENCE.md` synchronized with frontmatter; a regression test compares both. |
| Pre-push hook claim | ✅ Fixed | README now describes CI and `pre-commit`; no pre-push claim. |
| GEN8 "implemented" with unchecked boxes | ✅ Fixed | Status changed to "Partially implemented"; unchecked items are explicitly open work. |
| `qa-docker` / `testing-standards` overlap | ✅ Fixed | Docker and mock guidance merged into `testing-standards`; `qa-docker` removed and all references updated. |

## Verification performed

```bash
# Framework (from .agent/)
python tools/forge.py --version                 # agentic-forge 1.4.0
ruff check tools tests                          # 0 findings (Ruff 0.17.1)
ruff format --check tools tests                 # 19 files already formatted
mypy tools tests                                # 0 issues
pytest tests -q                                 # 32 passed
python tools/forge.py validate                  # 17 skills, 14 workflows, 3 templates
python tools/forge.py validate --graph          # exit 0
python tools/forge.py validate --conflicts      # exit 0
python tools/forge.py memory check              # exit 0
bash scripts/ci.sh                              # exit 0 in a clean venv
```

Standalone-framework mode (no `forge.toml` in the parent) was also exercised:
`validate` reports 11 skills, 14 workflows and 3 templates; only optional
project-state warnings remain (exit 0).

## Rollout

1. `agentic-forge` is published at `v1.4.1` (supersedes `v1.4.0`).
2. Update each sibling pin:
   ```bash
   git -C .agent fetch --tags
   git -C .agent checkout v1.4.1
   git add .agent
   git commit -m "chore(agent): bump agentic-forge to v1.4.1"
   ```
3. Run `forge.py validate`, `validate --graph`, `validate --conflicts`,
   `metrics validate`, `memory check` and `memory prune` in each repository.
4. Replace any custom `qa-docker` references with `testing-standards`.
5. `qgis-plugin-manager` has a **local framework fork** in its submodule
   (project commands, tests and requirements that are now upstreamed). Reconcile
   or discard that local diff before pinning `v1.4.1`; do not run
   `git submodule update` there first.

### Deployment helper

The repository ships a safe helper that refuses dirty worktrees, validates the
new pin and rolls back on failure:

```bash
# Dry-run: show current and desired framework versions
./scripts/deploy_agentic_forge.sh ~/qgispluginsdev/sec_interp

# Apply: fetch, checkout, run all gates and commit the submodule pin
./scripts/deploy_agentic_forge.sh ~/qgispluginsdev/sec_interp --apply
```

### Deployment status (2026-10-18)

| Repository | Status |
| :--- | :--- |
| `ai-context-core` | ✅ Pinned to `v1.4.1` and pushed. |
| `sec_interp` | ✅ v1.4.1 simulation green (overlay workflows, metrics, memory check); apply the helper with `--apply` from a normal shell. |
| `qgis-plugin-manager` | ⚠️ Dirty local framework fork; the helper refuses until it is reconciled. |
| `qgis-plugin-analyzer`, `sistema_agent_ai`, `antigravity-*` | — No `.agent` submodule; no action. |

## Rollback

```bash
git -C .agent checkout v1.3.0
git add .agent
git commit -m "chore(agent): roll back agentic-forge to v1.3.0"
```
