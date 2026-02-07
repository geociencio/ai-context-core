import unittest
import ast
from ai_context_core.analyzer.summarizers.issues import IssuesSummarizer
from ai_context_core.analyzer.summarizers.git_patterns import GitPatternsSummarizer
from ai_context_core.analyzer.patterns_detectors.observer_components.signals import (
    detect_signals,
)
from ai_context_core.analyzer.metrics import calculate_halstead_metrics


class TestCoverageBoost(unittest.TestCase):
    def test_issues_summarizer(self):
        analyses = {
            "security": [
                {"module": "auth.py", "total_issues": 2, "max_severity": "high"}
            ],
            "debt": [
                {"module": "legacy.py", "total_issues": 10, "severity_score": 5},
                {"module": "minor.py", "total_issues": 1, "severity_score": 2},
            ],
            "dependencies": {"circular_dependencies": [["a", "b", "a"]]},
            "optimizations": [
                {"module": "api.py", "suggestions": [{"message": "Use async"}]}
            ],
        }
        summarizer = IssuesSummarizer(analyses)
        issues_text = summarizer.build_issues()
        recs_text = summarizer.build_recommendations()

        self.assertIn("Security Issues", issues_text)
        self.assertIn("auth.py", issues_text)
        self.assertIn("Technical Debt", issues_text)
        self.assertIn("legacy.py", issues_text)
        self.assertNotIn("minor.py", issues_text)  # Score < 4
        self.assertIn("Circular Dependencies", issues_text)
        self.assertIn("a -> b -> a", issues_text)

        self.assertIn("api.py", recs_text)
        self.assertIn("Use async", recs_text)

    def test_git_patterns_summarizer(self):
        analyses = {
            "git": {
                "churn": {
                    "available": True,
                    "period_days": 30,
                    "files_changed": 5,
                    "added": 100,
                    "deleted": 20,
                    "total_churn": 120,
                },
                "hotspots": [{"path": "core.py", "commits": 50}],
            },
            "patterns": {
                "Singleton": [
                    {"class": "Database", "module": "db.py", "confidence": 100}
                ]
            },
        }
        summarizer = GitPatternsSummarizer(analyses)
        git_text = summarizer.build_git()
        pats_text = summarizer.build_patterns()

        self.assertIn("Code Churn", git_text)
        self.assertIn("Hotspots", git_text)
        self.assertIn("core.py", git_text)
        self.assertIn("Singleton", pats_text)
        self.assertIn("Database", pats_text)

    def test_detect_signals(self):
        code = """
class MyWidget:
    clicked = pyqtSignal()
    changed = QtCore.pyqtSignal(int)
    custom = Signal()
    data = 123  # Not a signal
"""
        tree = ast.parse(code)
        # We need the ClassDef node
        class_node = tree.body[0]
        count = detect_signals(class_node)
        self.assertEqual(count, 3)

    def test_halstead_metrics(self):
        # n1=4, n2=6, N1=10, N2=15
        metrics = calculate_halstead_metrics(4, 6, 10, 15)
        self.assertIn("volume", metrics)
        self.assertIn("difficulty", metrics)
        self.assertIn("effort", metrics)
        # V = N * log2(n) = 25 * log2(10) ~= 25 * 3.32 ~= 83
        self.assertGreater(metrics["volume"], 80)
        # D = (n1/2) * (N2/n2) = (4/2) * (15/6) = 2 * 2.5 = 5
        self.assertEqual(metrics["difficulty"], 5.0)

    def test_context_extractor(self):
        from ai_context_core.context.components.extractor import ContextExtractor

        contexts = {
            "file1.py": "def hello(): pass",
            "metadata": {"version": "1.0.0", "author": "John"},
            "ignored": "something else",
        }
        # Keyword "hello" should match file1.py
        res = ContextExtractor.extract_relevant("Please check hello function", contexts)
        self.assertIn("file1.py", res)
        self.assertIn("def hello()", res)

        # Keyword "author" should match metadata (json dumped)
        res = ContextExtractor.extract_relevant("Who is author", contexts)
        self.assertIn("metadata", res)
        self.assertIn("John", res)

        # No match
        res = ContextExtractor.extract_relevant("XYZ", contexts)
        self.assertEqual(res, "No relevant context.")

    def test_update_context_file(self):
        import shutil
        import tempfile
        import pathlib
        import yaml
        from ai_context_core.context.components.store_components.updaters import (
            update_context_file,
        )

        tmp_dir = tempfile.mkdtemp()
        try:
            p = pathlib.Path(tmp_dir)
            updates_file = p / ".ai-context-updates.yaml"

            # 1. First update (create file)
            update_context_file(p, {"new_v": [1, 2]})
            data = yaml.safe_load(updates_file.read_text())
            self.assertEqual(data["new_v"], [1, 2])

            # 2. Update with list extension
            update_context_file(p, {"new_v": [3]})
            data = yaml.safe_load(updates_file.read_text())
            self.assertEqual(data["new_v"], [1, 2, 3])

            # 3. Update with dict merge
            update_context_file(p, {"meta": {"a": 1}})
            update_context_file(p, {"meta": {"b": 2}})
            data = yaml.safe_load(updates_file.read_text())
            self.assertEqual(data["meta"], {"a": 1, "b": 2})

            # 4. Overwrite
            update_context_file(p, {"meta": "overwritten"})
            data = yaml.safe_load(updates_file.read_text())
            self.assertEqual(data["meta"], "overwritten")

        finally:
            shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
