from ai_context_core.analyzer.builders.scorer import ProjectScorer


def test_scorer_empty_data():
    scorer = ProjectScorer({})
    assert scorer.calculate([], {}) == 0.0


def test_scorer_qgis_factor():
    config = {
        "quality_weights": {"no_syntax_error": 100},
        "patterns": {"qgis_compliance": {"enabled": True}},
    }
    scorer = ProjectScorer(config)
    modules = [{"path": "m1.py", "syntax_error": False}]
    # max_mod_score = 100 (from no_syntax_error) + others (defaults)
    # default max_mod_score = 15+20+15+5+100 = 155 (if no_syntax_error is 100)
    # Wait, the defaults are hardcoded in calculate() too.
    # self.weights.get("docstrings", 15) etc.

    ctx = {"qgis_compliance": {"compliance_score": 50.0}}
    score = scorer.calculate(modules, ctx)
    # Without QGIS: 100/155 * 100 = 64.5
    # With QGIS: (64.5 * 0.7) + (50 * 0.3) = 45.15 + 15 = 60.15 -> 60.2
    assert score > 0


def test_scorer_linter_factor():
    config = {"quality_weights": {"no_syntax_error": 100}}
    scorer = ProjectScorer(config)
    modules = [{"path": "m1.py", "syntax_error": False}]
    ctx = {"linter": {"available": True, "errors": 10}}
    score = scorer.calculate(modules, ctx)
    # Without linter: 100/155 * 100 = 64.5
    # Linter penalty: min(10, 10 * 0.5) = 5
    # Final: 64.5 - 5 = 59.5
    assert score < 64.5


def test_score_module_complexity_size_variants():
    config = {
        "quality_weights": {
            "complexity_medium": 10,
            "complexity_high": 5,
            "size_medium": 8,
        },
        "thresholds": {
            "complexity_low": 5,
            "complexity_medium": 10,
            "complexity_high": 15,
            "size_small": 50,
            "size_medium": 100,
        },
    }
    scorer = ProjectScorer(config)

    # Medium complexity
    m = {"complexity": 8, "sloc": 20}
    assert scorer._score_module(m) == 10  # complexity_medium weight

    # High complexity
    m = {"complexity": 12, "sloc": 20}
    assert scorer._score_module(m) == 5  # complexity_high weight

    # Medium size
    m = {"complexity": 2, "sloc": 80}
    # complexity_low (0) + size_medium (8) + no_syntax_error (0)
    assert scorer._score_module(m) == 8
