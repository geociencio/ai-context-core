"""Packaging regressions for the supported Python range."""

import pathlib

try:  # Python 3.11+
    import tomllib
except ImportError:  # pragma: no cover - exercised on Python 3.9/3.10
    import tomli as tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_tomli_declared_for_python_before_311():
    """The TOML fallback must be installed on Python 3.9/3.10.

    ``config_loader`` uses ``tomllib`` on 3.11+ and falls back to ``tomli`` on
    older interpreters. Without the conditional dependency, ``defaults.toml``
    is silently ignored on the oldest supported Python versions.
    """
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data["project"]["dependencies"]

    tomli_deps = [dep for dep in dependencies if dep.startswith("tomli")]
    assert tomli_deps, "tomli must be declared for python_version < '3.11'"
    assert any("3.11" in dep for dep in tomli_deps), tomli_deps
