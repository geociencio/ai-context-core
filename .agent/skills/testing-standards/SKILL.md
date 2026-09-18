---
name: testing-standards
description: Automated testing with pytest and Docker for ai-context-core.
trigger: when writing/executing tests, designing testing strategies, or configuring CI.
---

# Testing Standards

Defines requirements and best practices for testing, prioritizing environment consistency and execution speed.

## When to use this skill
- When creating new features (TDD or post-implementation).
- When refactoring critical logic.
- Before pushing changes to the repository.
- During the VERIFICATION phase of an agentic workflow.

## Degree of Freedom
- **Strict**: Docker (`make docker-test`) is mandatory for final validation.

## Workflow
1. **Design**: Write tests with `pytest` (both pytest-style and `unittest.TestCase` are accepted).
2. **Local run**: Quick feedback with `uv run pytest -q`.
3. **Final validation**: Run in an isolated environment with `make docker-test`.
4. **Analyze**: Verify coverage meets thresholds.

## Instructions and Rules

### 1. Framework and Runner
- **Runner**: `pytest` (for better reports and coverage tooling).
- **Location**: All tests in `tests/`.
- **Naming**: Files prefixed with `test_` (e.g. `test_engine.py`).

### 2. Isolation
- **Isolation**: Unit tests must run quickly without external dependencies (network, databases).
- **Mocks**: Use `unittest.mock` to isolate external dependencies (filesystem, git).
- **Cleanup**: Use `tempfile` and clean up after execution.

### 3. Coverage and Quality
- **Global threshold**: Minimum 70% coverage.
- **Critical paths**: `engine.py` and visitor core should target >80%.
- **Regression tests**: Add a regression test for every bug fixed.

## Quality Checklist
- [ ] Do tests run with `make docker-test`?
- [ ] Is the 70% coverage threshold met?
- [ ] Are mocks used for external dependencies?
- [ ] Does the code follow `test_*.py` naming?
- [ ] Was a regression test added for each bug fix?
