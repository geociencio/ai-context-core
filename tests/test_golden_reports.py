"""Golden-file smoke test for the end-to-end report pipeline (Phase 4.3)."""

import pathlib
import shutil

from ai_context_core.analyzer.engine import ProjectAnalyzer

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "golden_plugin"
GOLDEN = pathlib.Path(__file__).parent / "fixtures" / "golden_expected"


def _normalize(text: str) -> str:
    """Normalize volatile fields so golden comparisons stay stable."""
    lines = []
    for line in text.splitlines():
        if line.startswith("Analysis Date:"):
            line = "Analysis Date: <normalized>"
        elif line.startswith("Analyzer Version:"):
            line = "Analyzer Version: <normalized>"
        lines.append(line.rstrip())
    return "\n".join(lines).strip() + "\n"


def _generate(tmp_path, name: str) -> str:
    proj = tmp_path / "golden_plugin"
    shutil.copytree(FIXTURE, proj)
    ProjectAnalyzer(str(proj), ignore_cache=True).analyze()
    return _normalize((proj / name).read_text(encoding="utf-8"))


def test_golden_project_summary(tmp_path):
    got = _generate(tmp_path, "PROJECT_SUMMARY.md")
    expected = _normalize((GOLDEN / "PROJECT_SUMMARY.md").read_text(encoding="utf-8"))
    assert got == expected


def test_golden_ai_context(tmp_path):
    got = _generate(tmp_path, "AI_CONTEXT.md")
    expected = _normalize((GOLDEN / "AI_CONTEXT.md").read_text(encoding="utf-8"))
    assert got == expected
