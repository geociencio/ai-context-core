"""AI-driven recommendation engine using local heuristics.

This module provides "smart" recommendations for code improvements based on
static analysis metrics, without requiring external LLM API calls.
"""

from typing import Dict, Any, List


class AIRecommender:
    """Heuristic-based recommendation engine."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.thresholds = self.config.get("thresholds", {})

    def analyze_codebase(
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generates recommendations based on the full analysis results.

        Args:
            analysis_results: The complete aggregated analysis dictionary.

        Returns:
            A list of recommendation dictionaries.
        """
        recommendations = []

        # extracted for easier access
        analysis_results.get("complexity", {}).get("most_complex_modules", [])
        metrics = analysis_results.get("metrics", {})

        # 1. Project-level Recommendations
        self._check_overall_quality(metrics, recommendations)
        self._check_documentation_health(metrics, recommendations)
        self._check_testing_status(metrics, recommendations)

        # 2. Module-level Recommendations can be refined here if needed
        # (Though checks are mostly done in issues.py, we can add "high-level" strategy here)

        return recommendations

    def _check_overall_quality(
        self, metrics: Dict[str, Any], recs: List[Dict[str, Any]]
    ):
        """Checks overall project quality score."""
        score = metrics.get("quality_score", 0)
        if score < 50:
            recs.append(
                {
                    "category": "Project Health",
                    "priority": "Critical",
                    "message": f"Project Quality Score is low ({score}/100). Focus on reducing complexity and complying with standards.",
                }
            )
        elif score < 70:
            recs.append(
                {
                    "category": "Project Health",
                    "priority": "High",
                    "message": f"Project Quality Score ({score}/100) has room for improvement. Target complexity reduction.",
                }
            )

    def _check_documentation_health(
        self, metrics: Dict[str, Any], recs: List[Dict[str, Any]]
    ):
        """Checks documentation coverage."""
        cov = metrics.get("docstring_coverage", 0)
        if cov < 50:
            recs.append(
                {
                    "category": "Documentation",
                    "priority": "Medium",
                    "message": f"Documentation coverage is low ({cov}%). Consider enforcing docstrings in CI.",
                }
            )

    def _check_testing_status(
        self, metrics: Dict[str, Any], recs: List[Dict[str, Any]]
    ):
        """Checks testing ratios."""
        test_count = metrics.get("test_files_count", 0)
        _total_modules = metrics.get("entry_points_count", 0) + 5  # rough estimate base
        # Better: use actual module count from structure
        # skipping exact math for safety, just checking if explicit 0
        if test_count == 0:
            recs.append(
                {
                    "category": "Testing",
                    "priority": "Critical",
                    "message": "No test files detected. Initialize a test suite immediately.",
                }
            )

    def analyze_module(self, module_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyzes a single module for specific refactoring recommendations.

        This can replace or augment issues.find_optimizations.
        """
        suggestions = []

        # Complexity
        cc = module_data.get("complexity", 0)
        if cc > 30:
            suggestions.append(
                {
                    "type": "refactoring",
                    "message": f"Critical Complexity ({cc}). Split this module into smaller components immediately.",
                }
            )
        elif cc > 15:
            suggestions.append(
                {
                    "type": "refactoring",
                    "message": f"High Complexity ({cc}). Consider extracting logic to helper functions.",
                }
            )

        # Maintenance Index
        mi = module_data.get("maintenance_index", 100)
        if mi < 50:
            suggestions.append(
                {
                    "type": "maintenance",
                    "message": f"Low Maintainability ({mi}). Hard to maintain code detected.",
                }
            )

        return suggestions
