"""Regression tests for --include-md / context_docs (Phase 4.2)."""

from ai_context_core.analyzer.engine import ProjectAnalyzer
from ai_context_core.analyzer.providers.context_fields import read_manual_notes


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _notes(analyzer: ProjectAnalyzer) -> str:
    return read_manual_notes(analyzer.project_path, analyzer.config, analyzer.include_md)


def test_context_docs_config_is_embedded(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n\nSome notes.\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": ["ARCHITECTURE.md"]}, ignore_cache=True
    )
    notes = _notes(analyzer)

    assert "### ARCHITECTURE.md" in notes
    assert "Some notes." in notes


def test_include_md_globs_are_sorted_and_embedded(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "docs" / "a.md", "Alpha\n")
    _write(tmp_path / "docs" / "b.md", "Beta\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": []}, include_md=["docs/*.md"], ignore_cache=True
    )
    notes = _notes(analyzer)

    assert "Alpha" in notes and "Beta" in notes
    assert notes.index("a.md") < notes.index("b.md")


def test_base_notes_still_read(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / ".ai-context" / "project_brain.md", "Brain notes\n")

    analyzer = ProjectAnalyzer(str(tmp_path), config={"context_docs": []}, ignore_cache=True)
    assert "Brain notes" in _notes(analyzer)


def test_analyze_embeds_docs_in_ai_context(tmp_path):
    from ai_context_core.sources.pipeline import compile_context, render_context

    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "ARCHITECTURE.md", "# Arch\n\nDESIGN_TOKEN\n")

    result = compile_context(
        tmp_path, {"context_docs": ["ARCHITECTURE.md"]}, "builtin", ignore_cache=True
    )
    render_context(result, tmp_path, {"context_docs": ["ARCHITECTURE.md"]})

    ai_context = (tmp_path / "AI_CONTEXT.md").read_text(encoding="utf-8")
    assert "MANUAL ARCHITECTURE NOTES" in ai_context
    assert "DESIGN_TOKEN" in ai_context
