---
description: How to commit changes cleanly (handling hooks)
agent: qa_engineer
skills: [testing-standards, commit-standards, agentic-memory]
validation: |
  - Verify that ruff passes without errors
  - Confirm that ai-ctx analyze runs successfully
  - Validate that the commit message follows Conventional Commits
---

# Workflow: Create Commit

Commits changes while ensuring code quality standards are met without getting blocked by pre-commit hook conflicts.

### 1. Preparation and Cleanup (Automatic)
```bash
uv run ruff check --fix .
uv run ruff format .
```

### 2. Stage Changes
```bash
git add .
```

### 3. Quality Synchronization (Guardian)
```bash
uv run ai-ctx analyze --path .
```

🤖 **Agent Action**: Analyze quality metrics and alert if cyclomatic complexity increased, docstring coverage decreased, or new compliance violations were detected.

### 4. Message Proposal (AI-Assisted)

🤖 **Agent Action**: Use `commit-standards` to:
- Analyze staged changes (`git diff --cached`)
- Generate 2-3 message options following Conventional Commits
- Validate format: correct type, appropriate scope, English, imperative
- Alert on breaking changes requiring `!` or footer

### 4.5 Quality Reflection (Auditor Check)
- **Agent Reflection**: Activate the `@auditor` role.
- **Diff Analysis**: Contrast the message with `git diff --cached`.
- **Validation**: Ensure no leakage of debug code (`print`, TODOs, commented logic).
- **Consolidation**: Verify the commit is a "clean unit of value".

### 5. Commit
```bash
git commit -m "type(scope): description" -m "detailed body"
```

*If the pre-commit hook persists in failing:* review errors, `git add` again, repeat the commit.

### 6. Structured Completion
```yaml
commit_status: success
files_changed: [list]
conventional_type: fix | feat | docs | style | etc
tests_verified: true/false
```

**Philosophy**: Each commit is a clean unit of value, documented and metrically validated.
