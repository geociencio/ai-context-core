import unittest
import pathlib
from unittest.mock import patch
from ai_context_core.analyzer.providers.analyzer import GitAnalyzer


class TestGitAnalysis(unittest.TestCase):
    def setUp(self):
        self.project_path = pathlib.Path(__file__).parent.parent.resolve()

    def test_is_repo(self):
        # Test positive case (is a repo)
        with patch("ai_context_core.analyzer.providers.analyzer.GitRunner.run") as mock_run:
            mock_run.return_value = "true\n"
            self.assertTrue(GitAnalyzer(self.project_path).is_repo())

        # Test negative case (is not a repo)
        with patch("ai_context_core.analyzer.providers.analyzer.GitRunner.run") as mock_run:
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

    def test_parse_churn_numstat_with_rename(self):
        from ai_context_core.analyzer.providers.parser import GitParser

        output = "10\t2\tcore/logic.py\n0\t0\t{old => new}/moved.py\n3\t1\tcore/logic.py\n"
        churn = GitParser.parse_churn(output, 30)

        self.assertTrue(churn["available"])
        self.assertEqual(churn["files_changed"], 2)
        self.assertEqual(churn["added"], 13)
        self.assertEqual(churn["deleted"], 3)
        self.assertEqual(churn["total_churn"], 16)
        self.assertEqual(churn["per_file"]["core/logic.py"], {"added": 13, "deleted": 3})
        self.assertEqual(churn["per_file"]["new/moved.py"], {"added": 0, "deleted": 0})

    def test_parse_churn_empty(self):
        from ai_context_core.analyzer.providers.parser import GitParser

        self.assertEqual(GitParser.parse_churn("", 30), {"available": False})

    def test_filter_churn_scopes_to_analyzed_code(self):
        from ai_context_core.analyzer.providers.git_churn import filter_churn

        churn = {
            "available": True,
            "period_days": 30,
            "added": 100,
            "deleted": 50,
            "total_churn": 150,
            "files_changed": 2,
            "per_file": {
                "core/a.py": {"added": 60, "deleted": 20},
                "docs/x.md": {"added": 40, "deleted": 30},
            },
        }

        out = filter_churn(churn, lambda p: p.startswith("docs/"))

        self.assertEqual(out["per_file"], {"core/a.py": {"added": 60, "deleted": 20}})
        self.assertEqual(out["total_churn"], 80)
        self.assertEqual(out["files_changed"], 1)
        self.assertEqual(out["raw_total_churn"], 150)
        self.assertTrue(out["available"])

    def test_get_churn_uses_exclusion_patterns(self):
        import tempfile
        from ai_context_core.analyzer.providers.runner import GitRunner

        numstat = "10\t5\tsrc/a.py\n3\t2\tdocs/x.md\n"
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(GitRunner, "run", side_effect=["true\n", numstat]):
                churn = GitAnalyzer(pathlib.Path(tmp), ["docs"]).get_churn(days=7)

        self.assertEqual(churn["per_file"], {"src/a.py": {"added": 10, "deleted": 5}})
        self.assertEqual(churn["total_churn"], 15)
        self.assertEqual(churn["raw_total_churn"], 20)
        self.assertEqual(churn["files_changed"], 1)


if __name__ == "__main__":
    unittest.main()
