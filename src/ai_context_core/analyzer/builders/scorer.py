"""Weighted quality scoring for projects and modules."""

from typing import Dict, Any, List


class ProjectScorer:
    """Handles project quality score calculation using weighted metrics."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the scorer with configuration.

        Args:
            config: Configuration dictionary containing weights and thresholds.
        """
        self.weights = config.get("quality_weights", {})
        self.thresholds = config.get("thresholds", {})
        self.config = config

    def calculate(
        self, modules_data: List[Dict[str, Any]], ctx: Dict[str, Any]
    ) -> float:
        """Calculates the overall project quality score.

        Args:
            modules_data: List of analyzed modules.
            ctx: Global analysis context.

        Returns:
            Final quality score (0.0 - 100.0).
        """
        if not modules_data:
            return 0.0

        max_mod_score = (
            self.weights.get("docstrings", 15)
            + self.weights.get("complexity_low", 20)
            + self.weights.get("size_small", 15)
            + self.weights.get("has_main", 5)
            + self.weights.get("no_syntax_error", 25)
        )

        total, max_total = 0.0, len(modules_data) * max_mod_score
        for m in modules_data:
            total += self._score_module(m)

        score = (total / max_total * 100) if max_total > 0 else 0

        # Factor QGIS
        qgis_enabled = (
            self.config.get("patterns", {})
            .get("qgis_compliance", {})
            .get("enabled", False)
        )
        qgis_score = ctx.get("qgis_compliance", {}).get("compliance_score")
        if qgis_enabled and qgis_score is not None:
            score = (score * 0.7) + (qgis_score * 0.3)

        # Factor Linter
        linter = ctx.get("linter", {})
        if linter.get("available"):
            score = max(0, score - min(10, linter.get("errors", 0) * 0.5))

        return round(score, 1)

    def _score_module(self, m: Dict[str, Any]) -> int:
        """Scores an individual module based on quality indicators."""
        s = 0
        if m.get("docstrings", {}).get("module"):
            s += self.weights.get("docstrings", 0)

        c = m.get("complexity", 0)
        if c <= self.thresholds.get("complexity_low", 5):
            s += self.weights.get("complexity_low", 0)
        elif c <= self.thresholds.get("complexity_medium", 10):
            s += self.weights.get("complexity_medium", 0)
        elif c <= self.thresholds.get("complexity_high", 15):
            s += self.weights.get("complexity_high", 0)

        lines = m.get("sloc", m.get("lines", 0))
        if lines <= self.thresholds.get("size_small", 200):
            s += self.weights.get("size_small", 0)
        elif lines <= self.thresholds.get("size_medium", 400):
            s += self.weights.get("size_medium", 0)

        if m.get("has_main"):
            s += self.weights.get("has_main", 0)
        if not m.get("syntax_error"):
            s += self.weights.get("no_syntax_error", 0)
        return s
