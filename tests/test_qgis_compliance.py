import unittest
import ast
from src.ai_context_core.analyzer.ast_qgis import QGISComplianceVisitor


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

    def test_i18n_naming_patterns(self):
        code = """
class Patterns:
    def test(self):
        a = "snake_case_is_ignored"
        b = "camelCaseIsIgnored"
        c = "PascalCaseIsIgnored"
        d = "UPPER_CASE_IS_IGNORED"
        e = "This has spaces and is NOT ignored"
        f = "data.with.dots.is.ignored"
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        # f is dotted, a-d match patterns, e has spaces.
        # Only "This has spaces and is NOT ignored" should be counted.
        self.assertEqual(visitor.results["i18n_usage"]["total_strings"], 1)

    def test_i18n_dict_keys_ignored(self):
        code = """
cfg = {
    "technical_key": "Translated Value",
    "another_key": "Another Translated Value"
}
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        # 2 keys ignored, 2 values counted.
        self.assertEqual(visitor.results["i18n_usage"]["total_strings"], 2)

    def test_i18n_ignored_functions_expanded(self):
        code = """
obj.setObjectName("technical_name")
obj.addItem("Technical Item")  #addItem often used for UI, but guide says technical
obj.setValue("some_value")
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        # All these should be ignored because they are in the _ignored_functions list.
        self.assertEqual(visitor.results["i18n_usage"]["total_strings"], 0)

    def test_i18n_tr_simple(self):
        code = """
class Test:
    def __init__(self):
        self.tr('Hello World')
"""
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)

        self.assertEqual(visitor.results["i18n_usage"]["tr"], 1)
        self.assertEqual(visitor.results["i18n_usage"]["total_strings"], 1)

    def test_legacy_gdal_import(self):
        code = "import gdal"
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)
        self.assertEqual(visitor.results["gdal_import_style"], "Legacy")

    def test_correct_gdal_import(self):
        code = "from osgeo import gdal"
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)
        self.assertEqual(visitor.results["gdal_import_style"], "Correct")

    def test_qt_imports(self):
        code = "from PyQt5.QtCore import pyqtSignal\nimport PyQt6.QtWidgets"
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)
        self.assertIn("PyQt5.QtCore", visitor.results["qt_transition"]["pyqt5_imports"])
        self.assertIn(
            "PyQt6.QtWidgets", visitor.results["qt_transition"]["pyqt6_imports"]
        )

    def test_processing_framework(self):
        code = "class MyAlg(QgsProcessingAlgorithm): pass"
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)
        self.assertTrue(visitor.results["processing_framework"])

    def test_legacy_signals(self):
        code = "self.connect(self, SIGNAL('triggered()'), self.tab)"
        tree = ast.parse(code)
        visitor = QGISComplianceVisitor()
        visitor.visit(tree)
        self.assertEqual(visitor.results["signals_slots"]["legacy"], 1)


if __name__ == "__main__":
    unittest.main()
