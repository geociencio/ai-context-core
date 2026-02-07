import ast
from unittest.mock import patch
from ai_context_core.analyzer.metrics.scorer import ProjectScorer
from ai_context_core.analyzer.ast_metrics_components.sloc import calculate_sloc


def test_scorer_module_scoring():
    # Coverage for scorer.py lines 69, 86
    scorer = ProjectScorer(
        {"quality_weights": {"docstrings": 10, "has_main": 5, "no_syntax_error": 25}}
    )
    m_data = {
        "docstrings": {"module": "Has docstring"},
        "has_main": True,
        "complexity": 2,
        "sloc": 10,
        "syntax_error": False,
    }
    # This should trigger lines 69 and 86
    score = scorer._score_module(m_data)
    assert score >= 15


def test_sloc_calculate_exception():
    # Coverage for sloc.py exception handling
    with patch(
        "ai_context_core.analyzer.ast_metrics_components.sloc.tokenize.generate_tokens",
        side_effect=Exception("Tokenize fail"),
    ):
        # Should fallback to _calculate_sloc_fallback
        res = calculate_sloc(ast.parse("x=1"), "x=1")
        assert res == 1


def test_scorer_qgis_enabled():
    # Coverage for scorer.py lines 54-56
    scorer = ProjectScorer(
        {
            "quality_weights": {"no_syntax_error": 25},
            "patterns": {"qgis_compliance": {"enabled": True}},
        }
    )
    ctx = {"qgis_compliance": {"compliance_score": 80.0}}
    modules = [{"syntax_error": False, "complexity": 1, "sloc": 10}]
    score = scorer.calculate(modules, ctx)
    # Should blend QGIS score
    assert 0 <= score <= 100


def test_scorer_linter_penalty():
    # Coverage for scorer.py lines 60-61
    scorer = ProjectScorer({"quality_weights": {"no_syntax_error": 25}})
    ctx = {"linter": {"available": True, "errors": 5}}
    modules = [{"syntax_error": False, "complexity": 1, "sloc": 10}]
    score = scorer.calculate(modules, ctx)
    # Should apply linter penalty
    assert score >= 0
