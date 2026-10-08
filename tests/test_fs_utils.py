import unittest
from pathlib import Path
from ai_context_core.analyzer.providers import fs_utils
import tempfile
import shutil


class TestFsUtils(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.p_dir = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_exclusion_patterns(self):
        patterns = fs_utils.load_exclusion_patterns(self.p_dir)
        self.assertIn(".git", patterns)
        self.assertIn("__pycache__", patterns)


if __name__ == "__main__":
    unittest.main()
