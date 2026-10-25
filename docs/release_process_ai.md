---
description: Automated release workflow (tests, build, trusted publishing)
---

# Release Workflow for ai-context-core

Canonical release guide for **ai-context-core**. It describes how a version is
prepared, tagged, published on GitHub and uploaded to PyPI by
`.github/workflows/release.yml`.

> **Toolchain**: `uv` (build + lock), `pytest`, `ruff`, `gh`. `mypy` is not used.
> The version source of truth is `pyproject.toml`, mirrored in
> `src/ai_context_core/__init__.py` (fallback) and `uv.lock`.

---

## 0. How the pipeline works

```text
git push origin vX.Y.Z
        │
        ▼
[release.yml · draft-release]  →  GitHub Release (DRAFT)
        │  (maintainer publishes it)
        ▼
[release.yml · verify-build]   →  version guard + lint + tests + build + twine check
        │
        ▼
[release.yml · publish-pypi]   →  PyPI Trusted Publishing (OIDC)
        │
        ▼
[release.yml · attach-assets]  →  wheel + sdist attached to the GitHub Release
```

Publishing the draft is the **human approval gate**. After that, tests, build and
the PyPI upload are automatic.

---

## 1. One-time prerequisites

### PyPI Trusted Publishing

1. Sign in at <https://pypi.org>.
2. Project `ai-context-core` → **Publishing** → **Add a new publisher**.
3. Fill in the GitHub publisher:
   - **Owner**: `geociencio`
   - **Repository**: `ai-context-core`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`
4. Save. No API token is stored in GitHub.

### GitHub environment

Create **Settings → Environments → `pypi`**. Optionally require reviewers; the
workflow references this environment for the publish job.

> `PYPI_TOKEN` is no longer required. Remove it after a successful OIDC publish.

---

## 2. Prepare the release

1. **Quality gates**:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest -q
   uv run ai-ctx verify
   ```
2. **Bump the three version sites**:
   - `pyproject.toml` → `version`
   - `src/ai_context_core/__init__.py` → `__version__` fallback string
   - `uv.lock` → the `ai-context-core` package version
3. **Validate the guard**:
   ```bash
   uv run python scripts/check_release_version.py --tag vX.Y.Z
   ```
4. **Documentation**:
   - Move `[Unreleased]` in `CHANGELOG.md` to `[X.Y.Z] - YYYY-MM-DD`.
   - Create `docs/releases/notes/vX.Y.Z.md`.
   - Add an entry to `docs/DEVELOPMENT_LOG.md`.
5. **Sync agent metrics**:
   ```bash
   uv run python scripts/sync_metrics.py
   ```
6. **Commit** the release prep and generated artifacts separately:
   ```bash
   git add pyproject.toml uv.lock src/ai_context_core/__init__.py \
           CHANGELOG.md docs/DEVELOPMENT_LOG.md docs/releases/notes/vX.Y.Z.md
   git commit -m "chore(release): prepare vX.Y.Z"
   git add AI_CONTEXT.md PROJECT_SUMMARY.md project_context.json context_manifest.json
   git commit -m "chore(docs): regenerate context artifacts for vX.Y.Z"
   ```

---

## 3. Local build safety net (optional)

```bash
rm -rf dist
uv build
uv run twine check dist/*
```

The release workflow repeats this on the tag commit.

---

## 4. Tag and draft

```bash
git push origin main
git tag -a "vX.Y.Z" -m "Release vX.Y.Z"
git push origin "vX.Y.Z"
```

Pushing the tag triggers `draft-release`, which creates the GitHub Release in
**draft** mode using `docs/releases/notes/vX.Y.Z.md` (legacy names and a generic
fallback are supported).

---

## 5. Publish the draft (triggers automation)

```bash
gh release edit vX.Y.Z --draft=false --title "vX.Y.Z" \
  --notes-file docs/releases/notes/vX.Y.Z.md
```

Publishing fires `release: published` and the workflow runs:

1. `verify-build`: checkout the tag, install Python 3.11 + dev dependencies,
   `scripts/check_release_version.py`, Ruff, format, pytest, `ai-ctx verify`,
   `uv build`, `twine check`.
2. `publish-pypi`: Trusted Publishing with `pypa/gh-action-pypi-publish` and
   PEP 740 attestations. No token is used.
3. `attach-assets`: uploads `dist/*` to the GitHub Release.

Pre-releases are skipped by design; only stable releases reach PyPI.

---

## 6. Verify

```bash
gh run list --workflow=release.yml --limit 3
gh run view <run-id>        # verify-build, publish-pypi and attach-assets success
gh release view vX.Y.Z      # wheel + sdist assets
```

PyPI check:

```bash
python - <<'EOF'
import json, urllib.request
d = json.load(urllib.request.urlopen("https://pypi.org/pypi/ai-context-core/json"))
print("latest:", d["info"]["version"])
print("files:", [f["filename"] for f in d["releases"].get("X.Y.Z", [])])
EOF
```

---

## 7. Manual fallback

If GitHub Actions is unavailable, build locally and upload with your own PyPI
token. This bypasses Trusted Publishing and attachment automation:

```bash
rm -rf dist
uv build
uv run twine check dist/*
UV_PUBLISH_TOKEN=pypi-******** uv publish
```

Do not use the repository secret for local publishing; it is not readable
locally.

---

## 8. Troubleshooting

- **Version guard fails**: the tag, `pyproject.toml`, `__init__.py` fallback and
  `uv.lock` disagree. Fix all four and re-tag.
- **Trusted publishing fails**: verify the PyPI publisher uses workflow
  `release.yml` and environment `pypi`, and that the GitHub environment exists.
- **Release event uses the tag's workflow**: the workflow file is read from the
  tagged commit, not `main`. Fix the workflow before tagging, or move the tag if
  nothing has been published to PyPI.
- **PyPI upload succeeds but assets fail**: re-run only the failed
  `attach-assets` job.
- **Pre-release**: mark the GitHub release as pre-release; PyPI is skipped.

---

## ✅ Checklist

- [ ] Ruff, format, pytest and `ai-ctx verify` green.
- [ ] Three version sites updated and `scripts/check_release_version.py` passes.
- [ ] CHANGELOG, release notes, DEVELOPMENT_LOG and metrics synced.
- [ ] Release prep + generated artifacts committed.
- [ ] `uv build` + `twine check` green locally (optional).
- [ ] Tag `vX.Y.Z` pushed; GitHub draft created.
- [ ] Draft published; `verify-build`, `publish-pypi` and `attach-assets` success.
- [ ] Wheel + sdist visible on PyPI and attached to the GitHub Release.
