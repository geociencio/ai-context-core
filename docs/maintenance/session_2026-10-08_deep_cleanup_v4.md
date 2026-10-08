# Maintenance Session: 2026-10-08 — Deep Cleanup & v4.0.0 Release

Reference: [`.agent/next_steps.md`](../../.agent/next_steps.md) · [`docs/CHANGELOG.md`](../CHANGELOG.md)

## Technical Summary

Follow-up to the redundancy cleanup: a deep static audit surfaced one functional
bug, one architectural boundary violation, and a widespread metric-key contract
breach. This session fixed those, retired the remaining dead checker chain, and
shipped the result as the breaking **v4.0.0** release (GitHub release published;
PyPI upload left to the maintainer).

## Changes Made

### Anti-patterns surfaced (bug fix)
- `builders/aggregator.py` gained `_aggregate_antipatterns`, promoting
  `mod["antipatterns"]` to a project-level key. `PatternsBuilder` already read
  it, so God Object / Spaghetti / Magic Number / Dead Code detections now render
  in `AI_CONTEXT.md` (they were computed but never reported before).
- Golden fixture `tests/fixtures/golden_expected/AI_CONTEXT.md` regenerated;
  regression test added in `tests/test_aggregator_extended.py`.

### Dead code removed (Breaking)
- Deleted the dead `CheckerRegistry` chain: `visitors/checker_registry.py`,
  `visitors/security_checker.py`, `visitors/tech_debt_checker.py`,
  `visitors/debt.py`.
- Deleted the `analyzer/pattern_base.py` re-export facade.
- Removed unused symbols from `visitors/issues.py` (`run_analysis`,
  `find_security_issues`, `GenericIssueDetector`, `detect_ast_security_issues`)
  and `analyzer/registry.py` (`register_visitor`, `register_post_processor`,
  `get_checker_registry`).
- Kept `optimization_checker.py` (live via `find_optimizations`).

### Architecture purity
- Moved `secrets_scanner.py` (the only file-I/O module in `visitors/`) to
  `providers/`, keeping AST visitors side-effect free.

### Metric key contract
- `stats`, `analyze`, `ai_recommendations`, `context_metrics`,
  `summary_generator` now read project metrics via `metric_keys` constants.
- Complexity aggregation keys canonicalized in `builders/formatter.py`.

### Release
- Version bumped to `4.0.0` (`pyproject.toml`, `__init__.py`, `uv.lock`).
- Added `build` + `twine` to the `dev` dependency group.
- `ruff format .` applied (fixed the ~80-file drift).
- Tag `v4.0.0` pushed; GitHub release created with both build artifacts.

## Deliberately Deferred (to avoid regressions)

- **`X.py` + `X_rules.py` consolidation**: reverting/attempting a merge pushed
  `observer.py` to CC 37 (over the self-score budget of 25). The split is a
  deliberate complexity-management pattern, so only the dead legacy wrappers in
  `singleton_rules.py` and the `# noqa: F401` re-export hop in `observer_rules.py`
  were cleaned up.
- **Name-helper unification**: the four "resolve Name/Attribute" helpers have
  genuinely different semantics (leading vs trailing, lowercasing, Call
  recursion), so they were left untouched.

## Verification Results

- `uv run ruff check .` — clean; `ruff format --check .` — clean.
- `uv run pytest -q` — **299 passed** (local, Python 3.12).
- `make docker-test` — **299 passed** (Docker, Python 3.11).
- `uv run ai-ctx audit --threshold 70` — PASS (score 90.7).
- `uv run python scripts/validate_agent_system.py` — PASS.
- `uv run python -m build` + `uv run twine check dist/*` — PASSED.

## Impact

- Removed ~5 dead modules/facades and several dead symbols; net code reduction.
- Restored the visitor purity boundary (no file I/O in `visitors/`).
- Enforced the metric key contract across all CLI/builders consumers.
- Shipped `v4.0.0` (breaking) — GitHub release live.
