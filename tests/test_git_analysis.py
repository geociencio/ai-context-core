import unittest
import pathlib
from unittest.mock import patch
from ai_context_core.analyzer.providers.analyzer import GitAnalyzer


class TestGitAnalysis(unittest.TestCase):
    def setUp(self):
        self.project_path = pathlib.Path(__file__).parent.parent.resolve()

    def test_is_repo(self):
        # Test positive case (is a repo)
        with patch(
            "ai_context_core.analyzer.providers.analyzer.GitRunner.run"
        ) as mock_run:
            mock_run.return_value = "true\n"
            self.assertTrue(GitAnalyzer(self.project_path).is_repo())

        # Test negative case (is not a repo)
        with patch(
            "ai_context_core.analyzer.providers.analyzer.GitRunner.run"
        ) as mock_run:
            mock_run.return_value = None
            self.assertFalse(GitAnalyzer(pathlib.Path("/tmp")).is_repo())

    def test_get_hotspots(self):
        hotspots = GitAnalyzer(self.project_path).get_hotspots(limit=3)
        # Should return a list
        self.assertIsInstance(hotspots, list)
        if hotspots:
            self.assertIn("path", hotspots[0])
            self.assertIn("commits", hotspots[0])
            self.assertLessEqual(len(hotspots), 3)

    def test_get_churn(self):
        churn = GitAnalyzer(self.project_path).get_churn(days=7)
        self.assertIsInstance(churn, dict)
        if churn.get("available"):
            self.assertIn("total_churn", churn)
            self.assertIn("files_changed", churn)


if __name__ == "__main__":
    unittest.main()
