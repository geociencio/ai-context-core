---
name: debug-specialist
description: Systematic bug resolution via the scientific method.
trigger: when the user reports a bug, a test fails, or an anomaly is detected.
---

# Debug Specialist

Guides error resolution, avoiding quick patches and prioritizing stability and quality.

## When to use this skill
- When the user reports a bug or error.
- When a test fails unexpectedly.
- When an anomaly is detected in AST analysis.
- With unhandled exceptions in scripts.

## Degree of Freedom
- **Strict**: A reproduction test is mandatory before modifying source code.

## Workflow
1. **Isolate**: Identify the root cause by analyzing logs and tracebacks.
2. **Reproduce**: Create a new test in `tests/` that fails specifically due to this bug.
3. **Hypothesize**: Formulate a clear explanation of why the error occurs.
4. **Fix**: Apply the minimal fix respecting @coding-standards.
5. **Verify**: Run the new test and the full suite.
6. **Document**: Record the lesson in `.agent/memory/AGENT_LESSONS.md` if it is a recurring pattern.

## Instructions and Rules

### 1. No blind patches
- It is forbidden to modify code without understanding exactly why it fails.
- If the error is intermittent, use additional logging to capture state before fixing.

### 2. Test priority
- The fix is only successful if the reproduction test passes and `ai-ctx analyze` metrics do not degrade.

### 3. Cleanup
- Remove any temporary `print` or debug code before committing.

## Output (exact format)
- Diagnostic report: [Root Cause].
- Reproduction test: `tests/test_issue_XXX.py`.
- Fix applied in: [Module].
- Validation result: [PASS/FAIL].

## Quality Checklist
- [ ] Was a failing test created first?
- [ ] Does the fix respect `pathlib` and typing?
- [ ] Were regressions in other modules verified?
- [ ] Was the Quality Score maintained or improved?
- [ ] Was the lesson documented if applicable?
