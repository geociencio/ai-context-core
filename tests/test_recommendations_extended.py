import pytest
from ai_context_core.analyzer.builders.ai_recommendations import (
    RecommendationRule,
    DocumentationRule,
    TypeHintRule,
    AIRecommender,
    QualityScoreRule,
)
from ai_context_core.analyzer.constants import (
    AI_RECOMMENDATION_QUALITY_MEDIUM_THRESHOLD,
    COMPLEXITY_REFACTORING_THRESHOLD,
)


def test_recommendation_rule_abstract():
    # Coverage for RecommendationRule.check (line 29)
    rule = RecommendationRule()
    with pytest.raises(NotImplementedError):
        rule.check({})


def test_documentation_rule_full_coverage():
    # Coverage for DocumentationRule line 85 (return [] on high coverage)
    rule = DocumentationRule()
    assert rule.check({"docstring_coverage": 100}) == []


def test_type_hint_rule_full_coverage():
    # Coverage for TypeHintRule line 109 (return [] on high coverage)
    rule = TypeHintRule()
    assert rule.check({"type_hint_coverage": 100}) == []


def test_quality_score_rule_medium():
    # Coverage for QualityScoreRule line 53 (medium threshold)
    rule = QualityScoreRule()
    # Assuming threshold is around 70-80. Let's use 60.
    res = rule.check({"quality_score": AI_RECOMMENDATION_QUALITY_MEDIUM_THRESHOLD - 5})
    assert len(res) == 1
    assert "room for improvement" in res[0]["message"]


def test_ai_recommender_analyze_module_medium_complexity():
    # Coverage for AIRecommender.analyze_module line 177-178
    recommender = AIRecommender()
    module_data = {
        "complexity": COMPLEXITY_REFACTORING_THRESHOLD + 2,
        "maintenance_index": 100,
    }
    res = recommender.analyze_module(module_data)
    assert len(res) == 1
    assert "High Complexity" in res[0]["message"]


def test_ai_recommender_analyze_module_very_high_complexity():
    # Coverage for AIRecommender.analyze_module line 170-174
    from ai_context_core.analyzer.constants import VERY_HIGH_COMPLEXITY_THRESHOLD

    recommender = AIRecommender()
    module_data = {
        "complexity": VERY_HIGH_COMPLEXITY_THRESHOLD + 1,
        "maintenance_index": 100,
    }
    res = recommender.analyze_module(module_data)
    assert len(res) == 1
    assert "Critical Complexity" in res[0]["message"]
