---
description: Workflow to automatically correct linting and formatting issues
agent: qa_engineer
skills: [coding-standards, testing-standards]
validation: |
  - Verify that ruff passes without errors
  - Confirm that imports are sorted
---

# Workflow: Fix Linting

Automates the correction of style and code quality issues reported by static tools.

### 1. Initial Diagnosis
```bash
uv run ruff check .
```

### 2. Automatic Correction (Auto-Fix)
```bash
# 1. Sort imports
uv run ruff check --select I --fix .

# 2. Format code
uv run ruff format .

# 3. Apply general fixes (F401, E711, etc.)
uv run ruff check --fix .
```

### 3. Assisted Manual Correction
For errors that cannot be corrected automatically (e.g. `F821 Undefined name`):
1. Identify the file and line.
2. Apply a specific patch or manual edit.
3. Verify the correction does not break the logic.

### 4. Final Validation
```bash
uv run ruff check . && uv run ruff format --check .
uv run pytest -q
```

### 5. Cleanup Commit
```bash
git add .
git commit -m "style: apply automated linting fixes"
```
