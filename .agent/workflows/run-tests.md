---
description: How to run unit tests reliably
agent: qa_engineer
skills: [qa-docker, testing-standards]
validation: |
  - Verify that all tests pass
  - Confirm that there are no regressions
---

# Workflow: Run Tests

Ensures project stability is verified through unit and integration tests.

### 1. Run Tests (Local)
```bash
uv run pytest tests/ -v --cov=src/ai_context_core --cov-report=term-missing
```

### 2. Recommended Method (Docker - Complete)
The definitive health check runs all tests in an isolated Docker container:
```bash
make docker-test
```

**Key Notes:**
- Ensure `uv.lock` is synchronized before running tests (`uv sync`).
- Use `-x` to stop at the first error; `--ff` to run previously failed tests first.

🤖 **Agent Action**: Use `testing-standards` to interpret failures and validate the testing strategy.

## Expected Result
- Clear report of the project's stability status.
- Identification of regressions or environment-specific failures.
- Confirmation of whether the code is safe to integrate.

## Structured Result Summary
```yaml
test_run: complete
total_tests: [count]
passed: [count]
failed: [count]
coverage: [percentage]
```
