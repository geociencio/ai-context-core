"""AI-driven recommendation engine using local heuristics.

This module provides "smart" recommendations for code improvements based on
static analysis metrics, without requiring external LLM API calls.
"""

from typing import Dict, Any, List
from .constants import (
    AI_RECOMMENDATION_QUALITY_LOW_THRESHOLD,
    AI_RECOMMENDATION_QUALITY_MEDIUM_THRESHOLD,
    DOCSTRING_COVERAGE_THRESHOLD,
    VERY_HIGH_COMPLEXITY_THRESHOLD,
    COMPLEXITY_REFACTORING_THRESHOLD,
    MAINTENANCE_INDEX_THRESHOLD,
)


class RecommendationRule:
    """Base class for smart recommendation rules."""

    def check(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError


class QualityScoreRule(RecommendationRule):
    """Checks overall project quality score."""

    def check(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        score = metrics.get("quality_score", 0)
        if score < AI_RECOMMENDATION_QUALITY_LOW_THRESHOLD:
            return [
                {
                    "category": "Project Health",
                    "priority": "Critical",
                    "message": f"Quality Score is low ({score}/100).",
                }
            ]
        if score < AI_RECOMMENDATION_QUALITY_MEDIUM_THRESHOLD:
            return [
                {
                    "category": "Project Health",
                    "priority": "High",
                    "message": f"Quality Score ({score}/100) has room for improvement.",
                }
            ]
        return []


class DocumentationRule(RecommendationRule):
    """Checks documentation coverage."""

    def check(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        cov = metrics.get("docstring_coverage", 0)
        if cov < DOCSTRING_COVERAGE_THRESHOLD:
            return [
                {
                    "category": "Documentation",
                    "priority": "Medium",
                    "message": f"Low documentation coverage ({cov}%).",
                }
            ]
        return []


class TestingStatusRule(RecommendationRule):
    """Checks for presence of tests."""

    def check(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        if metrics.get("test_files_count", 0) == 0:
            return [
                {
                    "category": "Testing",
                    "priority": "Critical",
                    "message": "No test files detected. Initialize a test suite immediately.",
                }
            ]
        return []


class AIRecommender:
    """Heuristic-based recommendation engine."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.rules = [QualityScoreRule(), DocumentationRule(), TestingStatusRule()]

    def analyze_codebase(
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generates recommendations based on the full analysis results."""
        recs = []
        m = analysis_results.get("metrics", {})
        for rule in self.rules:
            recs.extend(rule.check(m))
        return recs

    def analyze_module(self, module_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyzes a single module for specific refactoring recommendations."""
        res = []
        cc = module_data.get("complexity", 0)
        if cc > VERY_HIGH_COMPLEXITY_THRESHOLD:
            res.append(
                {
                    "type": "refactoring",
                    "message": f"Critical Complexity ({cc}). Split this module.",
                }
            )
        elif cc > COMPLEXITY_REFACTORING_THRESHOLD:
            res.append(
                {
                    "type": "refactoring",
                    "message": f"High Complexity ({cc}). Extract logic.",
                }
            )

        mi = module_data.get("maintenance_index", 100)
        if mi < MAINTENANCE_INDEX_THRESHOLD:
            res.append(
                {"type": "maintenance", "message": f"Low Maintainability ({mi})."}
            )
        return res


def generate_recommendations(
    modules_data: List[Dict[str, Any]], project_metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Legacy wrapper for generating AI recommendations."""
    recommender = AIRecommender()
    return recommender.analyze_codebase({"metrics": project_metrics})
