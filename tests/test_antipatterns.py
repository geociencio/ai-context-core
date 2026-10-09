import unittest
import ast
from ai_context_core.analyzer.visitors import antipatterns


class TestAntipatterns(unittest.TestCase):
    def test_detect_god_object(self):
        # Create a class with 21 methods
        methods = "\n".join([f"    def m{i}(self): pass" for i in range(21)])
        code = f"""
class GodObject:
{methods}
"""
        tree = ast.parse(code)
        issues = antipatterns.detect_god_object(tree, threshold_methods=20)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["type"], "god_object")
        self.assertEqual(issues[0]["value"], 21)

    def test_detect_spaghetti_code(self):
        # Create a function with high complexity
        # if x: ... else: ... (Repeated 26 times)
        nested_ifs = "\n".join(["    if x: pass" for _ in range(26)])
        code = f"""
def spaghetti(x):
{nested_ifs}
"""
        tree = ast.parse(code)
        issues = antipatterns.detect_spaghetti_code(tree, complexity_threshold=25)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["type"], "spaghetti_code")
        self.assertGreater(issues[0]["value"], 25)

    def test_detect_magic_numbers(self):
        code = """
def calc(x):
    return x * 42
"""
        tree = ast.parse(code)
        issues = antipatterns.detect_magic_numbers(tree)
        self.assertGreaterEqual(len(issues), 1)
        self.assertEqual(issues[0]["value"], 42)

    def test_detect_dead_code(self):
        code = """
def unreachable():
    return True
    print("Unreachable")
"""
        tree = ast.parse(code)
        issues = antipatterns.detect_dead_code(tree)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["type"], "dead_code")

    def test_detect_magic_numbers_respects_allowlist(self):
        code = """
def calc(x):
    return x * 42 + 100
"""
        tree = ast.parse(code)
        tree.antipatterns_config = {"allowlist": [100]}
        issues = antipatterns.detect_magic_numbers(tree)
        values = {i["value"] for i in issues}
        self.assertIn(42, values)
        self.assertNotIn(100, values)

    def test_severity_rank_order(self):
        from ai_context_core.analyzer.visitors.antipattern_base import severity_rank

        self.assertLess(severity_rank("high"), severity_rank("medium"))
        self.assertLess(severity_rank("medium"), severity_rank("low"))

    def test_filter_issues_and_min_severity(self):
        from ai_context_core.analyzer.visitors.antipattern_base import (
            filter_issues,
            min_severity_from_config,
        )

        issues = [
            {"severity": "low", "message": "a"},
            {"severity": "high", "message": "b"},
        ]
        filtered = filter_issues(issues, "medium")
        self.assertEqual([i["message"] for i in filtered], ["b"])

        self.assertEqual(min_severity_from_config({}), "low")
        self.assertEqual(
            min_severity_from_config({"patterns": {"antipatterns": {"min_severity": "medium"}}}),
            "medium",
        )


if __name__ == "__main__":
    unittest.main()
