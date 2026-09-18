---
description: Unified process for releasing the Python package.
agent: qa_engineer
skills: [release-management, qa-docker, commit-standards]
validation:
  - Tests passing (Green)
  - Correct version in pyproject.toml
  - Build generated without errors (twine check OK)
---

Release workflow for `ai-context-core`.

1. **Preparation**:
   🤖 **Agent Action**: Use `release-management` to validate previous state.
   ```bash
   uv run ai-ctx audit --threshold 70
   uv run ruff check .
   ```

2. **Version & Docs Synchronization**:
    - Update `version` in `pyproject.toml` (and the fallback `__version__` in `src/ai_context_core/__init__.py`).
    - **Changelog**: Update `CHANGELOG.md` (use the `changelog-generator` skill to automate).
    - **Release Notes**: Create `docs/releases/notes/v[VERSION].md`.
    - **Development Log**: Add a milestone entry in `docs/DEVELOPMENT_LOG.md`.

3. **Technical Verification**:
   ```bash
   uv run pytest -q
   uv run ruff check .
   ```

4. **Git Operations**:
   ```bash
   git checkout main && git pull origin main
   git add pyproject.toml CHANGELOG.md README.md docs/ uv.lock
   git commit -m "chore(release): prepare v[VERSION]"
   git tag -a "v[VERSION]" -m "Release v[VERSION]"
   git push origin main --tags
   ```

5. **Build & Release**:
   ```bash
   rm -rf dist/
   uv run python -m build
   uv run twine check dist/*
   ```
   - **PyPI Upload**: `uv run twine upload dist/*` (or via CI).
   - **GitHub Release**: `gh release create v[VERSION] --title "v[VERSION]" --notes-file docs/releases/notes/v[VERSION].md dist/*`.
