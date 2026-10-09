import unittest
import ast
from ai_context_core.analyzer.visitors.ast_utils import detect_unused_imports
from ai_context_core.analyzer.builders.algorithms import GraphMetricsCalculator
from ai_context_core.analyzer.builders.dependencies import (
    detect_unused_imports_in_project,
)


class TestDependenciesAdvanced(unittest.TestCase):
    def test_detect_unused_imports(self):
        code = """
import os
import sys
from pathlib import Path

print(os.name)
"""
        tree = ast.parse(code)
        unused = detect_unused_imports(tree)
        self.assertIn("sys", unused)
        self.assertIn("pathlib.Path", unused)
        self.assertNotIn("os", unused)

    def test_detect_unused_imports_respects_all(self):
        import ast as _ast

        tree = _ast.parse("from .foo import Bar\nfrom .baz import Qux\n__all__ = ['Bar']\n")
        unused = detect_unused_imports(tree)
        self.assertFalse(any(u.endswith("Bar") for u in unused))
        self.assertTrue(any(u.endswith("Qux") for u in unused))

    def test_project_unused_imports_skips_package_reexports(self):
        modules = [
            {"path": "pkg/__init__.py", "unused_imports": ["pkg.a.A"]},
            {"path": "pkg/mod.py", "unused_imports": ["pkg.b.B"]},
        ]

        default = detect_unused_imports_in_project(modules)
        self.assertNotIn("pkg/__init__.py", default)
        self.assertIn("pkg/mod.py", default)

        strict = detect_unused_imports_in_project(
            modules, {"patterns": {"unused_imports": {"ignore_package_reexports": False}}}
        )
        self.assertIn("pkg/__init__.py", strict)

    def test_coupling_metrics(self):
        graph = {"A": {"B", "C"}, "B": {"C"}, "C": set()}
        metrics = GraphMetricsCalculator(graph).calculate_coupling_metrics()

        # A: fan_out=2, fan_in=0, cbo=2
        # B: fan_out=1, fan_in=1, cbo=2
        # C: fan_out=0, fan_in=2, cbo=2

        self.assertEqual(metrics["A"]["cbo"], 2)
        self.assertEqual(metrics["B"]["cbo"], 2)
        self.assertEqual(metrics["C"]["cbo"], 2)
        self.assertEqual(metrics["C"]["fan_in"], 2)


if __name__ == "__main__":
    unittest.main()
