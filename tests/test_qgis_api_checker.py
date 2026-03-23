import unittest
import ast
from ai_context_core.analyzer.visitors.qgis_api import QGISApiChecker


class TestQGISApiChecker(unittest.TestCase):
    def test_deprecated_apis(self):
        code = """
from qgis.core import QgsMapLayerRegistry
registry = QgsMapLayerRegistry.instance()
        """
        tree = ast.parse(code)
        results = {}
        checker = QGISApiChecker(results)

        for node in ast.walk(tree):
            checker.visit(node)

        issues = results["api_compatibility"]["deprecated_calls"]
        self.assertTrue(any(i["name"] == "QgsMapLayerRegistry" for i in issues))

    def test_qt6_incompatibilities(self):
        code = """
from PyQt5.QtCore import SIGNAL
obj.connect(obj, SIGNAL("clicked()"), lambda: print("legacy"))
        """
        tree = ast.parse(code)
        results = {}
        checker = QGISApiChecker(results)

        for node in ast.walk(tree):
            checker.visit(node)

        issues = results["api_compatibility"]["qt6_incompatibilities"]
        self.assertTrue(any(i["name"] == "SIGNAL" for i in issues))

    def test_best_practices(self):
        code = """
from PyQt5.QtCore import QSettings
settings = QSettings()
layer = iface.activeLayer()
        """
        tree = ast.parse(code)
        results = {}
        checker = QGISApiChecker(results)

        for node in ast.walk(tree):
            checker.visit(node)

        violations = results["api_compatibility"]["best_practice_violations"]
        self.assertTrue(any(v["name"] == "QSettings" for v in violations))
        self.assertTrue(any(v["name"] == "iface.activeLayer()" for v in violations))


if __name__ == "__main__":
    unittest.main()
