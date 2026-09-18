---
name: commit-standards
description: Clean, conventional commits with quality validation for ai-context-core.
trigger: when creating commits, reviewing pull requests, or preparing a release.
---

# Commit Standards

Ensures a clean, readable, and automatable Git history via Conventional Commits.

## When to use this skill
- Before committing.
- When reviewing pull requests.
- When preparing a new release.

## Degree of Freedom
- **Strict**: The `<type>(<scope>): <subject>` format is non-negotiable.

## Workflow
1. **Identify**: Determine the change type (`feat`, `fix`, `docs`, etc.).
2. **Scope**: Define the `scope` from the affected modules.
3. **Draft**: Write the message in English, present tense, imperative.
4. **Validate**: Run the `/create-commit` workflow when available.

## Instructions and Rules

### 1. Conventional Commits Format
- Structure: `<type>(<scope>): <subject>`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- **Scopes**: `analyzer`, `cli`, `builders`, `visitors`, `providers`, `config`, `docs`, `tests`.

### 2. Writing Rules
- **Language**: Commit message always in English.
- **Style**: Imperative mood, lowercase subject, no trailing period.

## Quality Checklist
- [ ] Does the message follow `type(scope): description`?
- [ ] Is the type one of the allowed values?
- [ ] Is the scope valid for the project?
- [ ] Is the message in English?
- [ ] Is it linked to an issue when necessary?
