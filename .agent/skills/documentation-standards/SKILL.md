---
name: documentation-standards
description: Standards for technical logs, session records, and project history.
trigger: when updating DEVELOPMENT_LOG.md, CHANGELOG.md, or creating session reports in docs/maintenance/.
---

# Documentation Standards

Defines the formats to ensure consistent, professional documentation across agents.

## 1. Session Log Maintenance

### 1.1 `docs/DEVELOPMENT_LOG.md`
Reverse chronological record of daily activity.

**Format:**
```markdown
## [YYYY-MM-DD] [SHORT TOPIC]
- **Achievement**: A sentence summarizing the main impact.
- **Changes**:
    - Relevant technical detail 1 (mention modules if applicable).
    - Relevant technical detail 2.
- **Quality**: Test status and ruff metrics.
- **Maintenance**: Link to the session log.
```

### 1.2 `docs/maintenance/session_*.md`
Detailed technical report of the session.

**Required structure:**
1. Title: `# Maintenance Session: YYYY-MM-DD - [Title]`
2. Technical summary (objective).
3. Changes made (categorized list).
4. Verification results (tests and linting).
5. Impact (technical consequence).

## 2. Writing Rules
1. **Language**: Content in English.
2. **Commit style**: Commits in English.
3. **Markdown**: Bold key terms; backticks for file/function names.
4. **Dates**: `YYYY-MM-DD` format.

## 3. Audit Checklist
- [ ] Used the `## [YYYY-MM-DD]` header correctly?
- [ ] Included the link to the corresponding session file?
- [ ] Is the tone technical and precise?
- [ ] Updated "Project History" for phase closures?
