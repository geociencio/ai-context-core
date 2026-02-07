import unittest
import ast
from src.ai_context_core.analyzer.ast_qgis import QGISComplianceVisitor
from src.ai_context_core.analyzer.aggregator import ResultsAggregator
from pathlib import Path


class TestQGISCompliance(unittest.TestCase):
    def test_i18n_usage_tr_and_translate(self):
        code = """
class MyPlugin:
    def __init__(self):
        self.tr("Hello")
        QCoreApplication.translate("Context", "World")
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        self.assertEqual(visitor.results["i18n_usage"]["tr"], 1)
        self.assertEqual(visitor.results["i18n_usage"]["translate"], 1)

    def test_total_strings_heuristics(self):
        code = """
import logging
logger = logging.getLogger(__name__)

class MyPlugin:
    def run(self):
        # Translatable
        msg = "This is a translatable string."
        
        # Ignored (Logger)
        logger.debug("Debug message should be ignored")
        logger.info("Info message should be ignored")
        
        # Ignored (Exceptions)
        raise ValueError("Technical error message")
        
        # Filtered (Paths/URLs/Placeholders)
        path = "/usr/bin/local"
        url = "https://example.com"
        placeholder = "{}"
        
        # Short strings
        short = "a"
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        # Only "This is a translatable string." should be counted.
        # Note: Depending on how "ValueError" is handled (Name vs Attribute),
        # it might need adjustment if it's called as `exceptions.ValueError`.
        self.assertEqual(visitor.results["i18n_usage"]["total_strings"], 1)

    def test_aggregator_i18n_sum(self):
        aggregator = ResultsAggregator(Path("/tmp"), {})
        m_data = [
            {
                "path": "mod1.py",
                "qgis_compliance": {
                    "i18n_usage": {"tr": 2, "translate": 1, "total_strings": 10}
                },
            },
            {
                "path": "mod2.py",
                "qgis_compliance": {
                    "i18n_usage": {"tr": 1, "translate": 2, "total_strings": 5}
                },
            },
        ]
        results = aggregator._aggregate_qgis_compliance(m_data, {})

        self.assertEqual(results["i18n_stats"]["total_tr"], 6)  # (2+1) + (1+2)
        self.assertEqual(results["i18n_stats"]["total_strings"], 15)


if __name__ == "__main__":
    unittest.main()
