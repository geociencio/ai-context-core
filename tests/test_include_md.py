"""Regression tests for --include-md / context_docs (Phase 4.2)."""

from ai_context_core.analyzer.engine import ProjectAnalyzer


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_context_docs_config_is_embedded(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "ARCHITECTURE.md", "# Architecture\n\nSome notes.\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": ["ARCHITECTURE.md"]}, ignore_cache=True
    )
    notes = analyzer._read_manual_notes()

    assert "### ARCHITECTURE.md" in notes
    assert "Some notes." in notes


def test_include_md_globs_are_sorted_and_embedded(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "docs" / "a.md", "Alpha\n")
    _write(tmp_path / "docs" / "b.md", "Beta\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": []}, include_md=["docs/*.md"], ignore_cache=True
    )
    notes = analyzer._read_manual_notes()

    assert "Alpha" in notes and "Beta" in notes
    assert notes.index("a.md") < notes.index("b.md")


def test_base_notes_still_read(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / ".ai-context" / "project_brain.md", "Brain notes\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": []}, ignore_cache=True
    )
    assert "Brain notes" in analyzer._read_manual_notes()


def test_analyze_embeds_docs_in_ai_context(tmp_path):
    _write(tmp_path / "app.py", "def f():\n    return 1\n")
    _write(tmp_path / "ARCHITECTURE.md", "# Arch\n\nDESIGN_TOKEN\n")

    analyzer = ProjectAnalyzer(
        str(tmp_path), config={"context_docs": ["ARCHITECTURE.md"]}, ignore_cache=True
    )
    analyzer.analyze()

    ai_context = (tmp_path / "AI_CONTEXT.md").read_text(encoding="utf-8")
    assert "MANUAL ARCHITECTURE NOTES" in ai_context
    assert "DESIGN_TOKEN" in ai_context
