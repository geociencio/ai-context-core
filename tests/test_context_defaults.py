"""Defaults and token-budget behavior for context rendering (v5.1.0, WS-3)."""

from ai_context_core.analyzer.builders.dependencies import DependencyBuilder
from ai_context_core.analyzer.builders.reporting import generate_dependency_diagram
from ai_context_core.analyzer.providers.config_loader import load_config
from ai_context_core.context.budget import budget_from_config


def _deps() -> dict:
    return {"import_graph": {"a.py": ["b.py"], "b.py": ["a.py"]}}


def test_defaults_enable_token_budget():
    """The shipped defaults cap the document and the dependencies section."""
    budget = budget_from_config(load_config())
    assert budget.max_tokens == 8000
    assert budget.per_section.get("dependencies") == 2500


def test_defaults_disable_mermaid_style():
    """Mermaid styling is off by default to keep AI_CONTEXT.md compact."""
    config = load_config()
    assert config["context"]["mermaid_style"] is False


def test_mermaid_style_is_optional():
    """The styling block is only emitted when explicitly requested."""
    deps = _deps()
    styled = generate_dependency_diagram(deps, include_style=True)
    compact = generate_dependency_diagram(deps, include_style=False)

    assert "classDef" in styled
    assert "classDef" not in compact
    assert "graph TD" in compact
    assert len(compact) < len(styled)


def test_dependency_builder_honors_mermaid_style():
    """DependencyBuilder reads ``[context].mermaid_style`` from its config."""
    analyses = {
        "dependencies": {
            "import_graph": {"a.py": ["b.py"]},
            "graph_metrics": {"nodes": 1, "edges": 1, "density": 1.0},
        }
    }

    plain: list = []
    DependencyBuilder(analyses, {"context": {"mermaid_style": False}}).build(plain)
    assert not any("classDef" in line for line in plain)

    decorated: list = []
    DependencyBuilder(analyses, {"context": {"mermaid_style": True}}).build(decorated)
    assert any("classDef" in line for line in decorated)
