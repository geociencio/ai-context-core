---
description: Guided workflow for code refactoring with complexity validation
agent: architect
skills: [domain-logic, coding-standards]
validation: |
  - Verify that cyclomatic complexity decreased
  - Confirm that tests still pass after refactoring
  - Validate that no architecture violations were introduced
---

# Workflow: Refactor Code

Guides code refactoring following project standards and specialized skill knowledge.

## When to Use This Workflow
- When `ai-ctx analyze` detects methods with high complexity.
- When `AI_CONTEXT.md` identifies critical technical debt.
- Before adding new features to complex modules.

## Refactoring Steps

1. **Identify Refactoring Target**:
   ```bash
   uv run ai-ctx analyze .
   ```
   🤖 **Agent Action**: Analyze `PROJECT_SUMMARY.md` to identify hotspots and technical debt.

2. **Load Specialized Context**:
   🤖 **Agent Action**: Load `domain-logic` or `coding-standards`.

3. **Apply Refactoring**:
   🤖 **Agent Action**: Apply SOLID principles and reduce cyclomatic complexity.

4. **Validate with Tests**:
   ```bash
   uv run pytest -q
   ```
   🤖 **Agent Action**: Ensure no regressions.

5. **Verify Quality Metrics**:
   ```bash
   uv run ai-ctx analyze .
   ```
   🤖 **Agent Action**: Confirm improvement in quality score and reduction in complexity.

5.5 **Complexity Audit (Auditor Reflection)**
   - Activate the `@auditor` role.
   - Ensure the refactor didn't hide complexity in "wrapper" functions.
   - Confirm adherence to project quality standards.

6. **Refactoring Commit**:
   Use `/create-commit` with a structured technical message.

## Expected Result
- More maintainable, testable code with reduced cyclomatic complexity.
- Zero functional regressions confirmed by tests.
- Technical documentation (docstrings) updated.
