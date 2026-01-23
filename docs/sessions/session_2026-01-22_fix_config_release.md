# Session Report - 2026-01-22

## Summary
Focused on fixing a critical configuration issue where `defaults.yaml` was missing from the installed package. Successfully diagnosed, fixed, and released **v1.0.1**.

## Key Achievements
- **Bug Fix**: Identified that `defaults.yaml` and template files were excluded from the build.
    - Added `MANIFEST.in` to explicitly include non-Python data files (`.yaml`, `.json`, `.md`, `.txt`).
    - Updated `pyproject.toml` to enable `include-package-data`.
- **Release v1.0.1**:
    - Bumped version to `1.0.1`.
    - Updated `CHANGELOG.md` and created release notes.
    - Tagged `v1.0.1` and built distribution artifacts.

## Next Steps
- Push changes and tag to origin to trigger PyPI publish workflow.
- Verify `sec_interp` integration with the new version.
