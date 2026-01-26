---
name: testing-standards
description: Guidelines for ensuring code stability through automated testing using Pytest and Docker.
---

# Testing Standards

This skill defines the requirements and best practices for testing within the `ai-context-core` project. We prioritize environment consistency and execution speed.

## 1. Test Framework & Runner

- **Authoring Style**: Tests are written using the standard `unittest` library (subclassing `unittest.TestCase`).
- **Execution Runner**: We use `pytest` as the test runner to leverage its superior CLI reporting, fixture management, and coverage tools.
- **Location**: All tests must reside in the `tests/` directory.
- **Naming**: Files must be prefixed with `test_` (e.g., `test_engine.py`).

## 2. Docker & Environment Isolation

All tests must be verifiable in an isolated containerized environment to replicate CI conditions.

- **Mandatory**: Use the project's `Makefile` to run tests via Docker.
  ```bash
  make docker-test
  ```
- **Local Dev**: You may run `uv run pytest` for quick feedback loops, but **final validation requires Docker**.

## 3. Coverage Requirements

- **Minimum Coverage**: The project maintains a threshold of **70%** code coverage.
- **Critical Paths**: Core logic in `engine.py` and `ast_utils.py` should aim for >80%.

## 4. Best Practices

- **Mocking**: Use `unittest.mock` to isolate external dependencies (e.g., file system, git operations).
- **Integration Tests**: Place slower tests that touch the disk or inspect multiple modules (like caching tests) in separate files (e.g., `test_integration_*.py`).
- **No Side Effects**: Tests must use temporary directories (`tempfile`) and clean up after themselves.
