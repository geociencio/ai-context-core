# Release {version} - {date}

Short Summary
-------------
A brief description (1-2 lines) of what is included in this release.

Highlights
----------
- Highlight 1 (new feature / improvement).
- Highlight 2 (important fix or security patch).

Notable Changes (Detailed)
----------------------------
- [PR #NNN](link) — feat: brief description of the improvement.
- [PR #MMM](link) — fix: brief description of the fixed bug.
- [PR #PPP](link) — docs: changes in documentation.

Security Fixes
-------------------------
- CVE / CVE-like notes (if applicable) and mitigation measures.
- Recommendation for affected users (update immediately, steps, etc.).

Breaking Changes
----------------------------------------------------
If applicable, detail:
- What changed.
- Why it was necessary.
- How to migrate (clear steps and commands).

Installation / Update Instructions
--------------------------------------------
- Installation from PyPI (when published):
  ```bash
  pip install ai-context-core=={version}
  ```
- Installation from GitHub (tarball / git):
  ```bash
  pip install git+https://github.com/geociencio/ai-context-core.git@v{version}
  ```

Published Artifacts
---------------------
- Wheels / sdist: link(s) or indicate that they are attached to the release.
- Binary / other assets: list of attached files.

Verifications Performed (CI)
------------------------------
- Links to GitHub Actions workflows that passed:
  - Build / Tests: <link to run>
  - Release draft: <link to run>
- List of manual tests performed (if applicable).

Changelog (entries per commit/PR)
----------------------------------
- commit/PR — short description (links).
- commit/PR — short description (links).

Contributors
--------------
Thanks to the following contributors for their input in this version:
- @jmbernales
(use PR or commit authors)

Additional Notes
-----------------
- Links to updated documentation (docs/).
- Warnings, post-release steps, or planning for future versions.

Checklist Before Publishing
---------------------------
- [ ] Automated tests pass on main.
- [ ] `CHANGELOG.md` updated.
- [ ] Version in `pyproject.toml` updated to {version}.
- [ ] Tag created: `git tag -a v{version} -m "Release v{version}"`
- [ ] Tag uploaded: `git push origin v{version}`
- [ ] Artifact build (`uv build`) and local verification.
- [ ] Publish to PyPI (if applicable): `uv publish`
- [ ] Create GitHub Release with this body (use `gh` or UI).
- [ ] Add assets to the Release (wheels / sdist) if available.
- [ ] Update badges in README (version / PyPI).

Suggested Commands
------------------
```bash
# Bump version in pyproject.toml
# Create tag and push
git commit -am "chore(release): v{version}"
git tag -a v{version} -m "Release v{version}"
git push origin main
git push origin v{version}

# Build artifacts
uv build

# Publish to PyPI (if applicable)
uv publish

# Create release using GitHub CLI (optional)
gh release create v{version} --title "v{version}" --notes-file .github/release_template.md dist/*
```

Example (execute upon publishing)
------------------------------
Title: Release v2.0.0 - Core Modularization & AI Optimization

Summary:
- Extracted core logic into standalone `ai-context-core` package.
- Standardized documentation to Google Style (>95% coverage).
- Added profiles for QGIS and generic Python projects.

(Add links to PRs and workflows supporting the release)
