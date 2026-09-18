---
name: release-management
description: Python package release process for ai-context-core.
trigger: when preparing releases, updating versions, or using /release-package.
---

# Release Management (Package Version)

Controls the version lifecycle of the `ai-context-core` package, ensuring quality and consistency in every delivery to PyPI/GitHub.

## When to use this skill
- At the end of a sprint or bug fix cycle.
- When updating `pyproject.toml` for a new version.
- When generating version notes or updating the changelog.

## Degree of Freedom
- **Strict**: Compliance with Semantic Versioning and quality checks is mandatory.

## Detailed Workflow

### Phase 1: Quality and Preparation
```bash
uv run ai-ctx audit --threshold 70
uv run ruff check .
```

### Phase 2: Versioning
1. Update `version` in `pyproject.toml`.
2. Add a `CHANGELOG.md` entry (Keep a Changelog format).
3. **Semver**: MAJOR (breaking CLI/API), MINOR (new rules/features), PATCH (bug fixes).

### Phase 3: Technical Verification
```bash
uv run pytest -q
```

### Phase 4: Git and Tagging
1. Release commit: `chore(release): prepare vX.Y.Z`.
2. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
3. Push: `git push origin main --tags`.

### Phase 5: Packaging and Distribution
```bash
rm -rf dist/ build/
uv run python -m build
uv run twine check dist/*
```
Then create the GitHub release (PyPI publication is typically via CI).

## Quality Checklist
- [ ] Does static analysis pass without critical errors?
- [ ] Is the version in `pyproject.toml` correct?
- [ ] Is `CHANGELOG.md` updated?
- [ ] Do tests pass locally?
