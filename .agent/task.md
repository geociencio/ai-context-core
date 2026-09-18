# Active Tasks — ai-context-core

This task board tracks the current development phase. Reference plan: `docs/maintenance/corrections_implementation_plan.md` and `docs/maintenance/developer_recommendations.md`.

## Phase: Agentic System Migration to Generation 8

- [x] Root `AGENTS.md` as SSoT (roles, skills matrix, workflows table) <!-- id: g8.1 -->
- [x] Native subagents in `opencode.json` (architect / qa_engineer / auditor) <!-- id: g8.2 -->
- [x] Retire `skill_sync.py`; add `scripts/validate_agent_system.py` <!-- id: g8.3 -->
- [x] Add `scripts/memory_prune.py` + `scripts/sync_metrics.py` <!-- id: g8.4 -->
- [x] 3-tier memory: `memory_policy.md`, `agent_metrics.json`, YAML lessons, `task.md` <!-- id: g8.5 -->
- [x] Skills: adapt 6 + create 8 new (English, frontmatter) <!-- id: g8.6 -->
- [x] Workflows: rename/align/create 11 + `index.md` <!-- id: g8.7 -->
- [x] System docs: `.agent/README.md` + `.agent/QUICK_REFERENCE.md` <!-- id: g8.8 -->

## Completed (recent)

- [x] Metric key contract unification (canonical `metric_keys.py`)
- [x] `# no-i18n` opt-out + punctuation heuristic
- [x] Observer signal detection hardening + safe dict access
- [x] Regression tests for patterns and `_match_path`
- [x] Metric labels renamed + documented vs `qgis-analyzer`

## Operational Status

- **Active Phase**: None (Gen 8 migration completed)
- **Current Metrics**: Tests 286/286 passing
