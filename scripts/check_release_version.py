#!/usr/bin/env python3
"""Validate that a release tag matches every version source."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.9/3.10
    import tomli as tomllib


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def collect_versions(root: Path) -> dict[str, str | None]:
    """Return the version from pyproject, uv.lock and the package fallback."""
    pyproject = _load_toml(root / "pyproject.toml")
    lock = _load_toml(root / "uv.lock")
    lock_versions = [
        package.get("version")
        for package in lock.get("package", [])
        if package.get("name") == "ai-context-core"
    ]
    init_text = (root / "src" / "ai_context_core" / "__init__.py").read_text(encoding="utf-8")
    fallback = re.search(r'__version__\s*=\s*"([^"]+)"', init_text)
    return {
        "pyproject": pyproject["project"]["version"],
        "lock": lock_versions[0] if lock_versions else None,
        "init": fallback.group(1) if fallback else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Release tag, e.g. v5.1.0")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    args = parser.parse_args()

    tag = args.tag.removeprefix("v")
    versions = collect_versions(args.root)
    values: dict[str, str | None] = {"tag": tag, **versions}

    print("Release version check:")
    for name, value in values.items():
        print(f"  {name}: {value}")

    if None in values.values() or len(set(values.values())) != 1:
        print("ERROR: tag and version sources do not match.", file=sys.stderr)
        return 1

    print(f"OK: all sources report {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
