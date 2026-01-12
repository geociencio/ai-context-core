---
description: Unified Release Workflow (Quality + Automation)
---

# Release Workflow for Ai-Context-Core

This document is the master guide for performing a project release. It combines rigorous Quality Assurance steps with automated CLI tools (`uv`, `sed`, `gh`) to ensure a robust and efficient process.

## Phase 1: Quality & Readiness
Before touching version numbers, validate the project state.

1. **Run Project Analyzer**:
   // turbo
   `uv run ai-ctx analyze`
   > [!NOTE]
   > Scores should ideally be high (>90%) for a release.

2. **Update Quality Badge**:
   - Check `PROJECT_SUMMARY.md` in the root.
   - Update `Code Score` and `Doc Coverage` badges in `README.md`.
   - Ensure **Docstring Coverage** is > 95%.

## Phase 2: Versioning & Documentation
1. **Determine Version**:
   - Check `pyproject.toml` and `ROADMAP.md`.
   - Decide next SemVer (Major/Minor/Patch).

2. **Bump Version (pyproject.toml)**:
   **Option A: Automated (sed)**
   ```bash
   # Example: 1.1.0 -> 1.2.0
   sed -i 's/^version = "1.1.0"/version = "1.2.0"/' pyproject.toml
   ```
   **Option B: Manual**
   - Edit `pyproject.toml` directly.

3. **Update CHANGELOG.md**:
   - Move `[Unreleased]` content to `[X.Y.Z] - YYYY-MM-DD`.
   - Ensure specific sections (`Added`, `Fixed`) are correct.

4. **Generate Release Notes**:
   ```bash
   VERSION=1.0.0
   mkdir -p docs/releases/notes
   sed -e "s/{version}/$VERSION/g" -e "s/{date}/$(date +%F)/g" .github/release_template.md > docs/releases/notes/v$VERSION.md
   ```
   > **Review**: Check `docs/releases/notes/v$VERSION.md` and fill in any placeholders.

## Phase 3: Verification
Ensure the codebase is clean and functional before tagging.

1. **Run Linting & Formatting**:
   // turbo
   `uv run ruff check .`
   // turbo
   `uv run ruff format .`
   - Fix any errors.

2. **Run Tests**:
   // turbo
   `uv run python -m unittest discover tests`
   - **Requirement**: 100% Pass Rate.

## Phase 4: Git Operations
1. **Commit Changes**:
   ```bash
   git add pyproject.toml CHANGELOG.md README.md
   git commit -m "chore(release): prepare v$VERSION"
   ```

2. **Create Tag**:
   ```bash
   git tag -a "v$VERSION" -m "Release v$VERSION"
   ```

3. **Push to Origin**:
   ```bash
   git push origin main
   git push origin "v$VERSION"
   ```

## Phase 5: Build & Distribution
1. **Build Artifacts**:
   ```bash
   uv build
   # Verify output in dist/
   ls -la dist/
   ```

2. **Create GitHub Release**:
   Use `gh` to create a Draft Release with assets attached.
   ```bash
   gh release create "v$VERSION" --title "v$VERSION" --notes-file /tmp/release_notes.md --draft
   gh release upload "v$VERSION" dist/* --clobber
   ```

3. **Publish (PyPI)**:
   - Go to GitHub -> Releases.
   - Edit the Draft.
   - Click **"Publish release"**.
   - *Note: This triggers the `release.yml` workflow to upload to PyPI automatically.*

---

## ✅ Quick Checklist
- [ ] Quality Analysis run (`ai-ctx analyze`) & Badge updated.
- [ ] Version bumped in `pyproject.toml`.
- [ ] `CHANGELOG.md` finalized.
- [ ] Tests and Linter passed.
- [ ] Git Tag created and pushed.
- [ ] Artifacts built (`uv build`).
- [ ] GitHub Draft Release created (with assets).
