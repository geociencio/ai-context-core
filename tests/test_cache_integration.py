import shutil
import tempfile
import pathlib
import json
from ai_context_core.analyzer import engine, fs_utils


class TestIncrementalCache:
    def setup_method(self):
        self.test_dir = pathlib.Path(tempfile.mkdtemp())
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir()

        # Create dummy python files
        (self.src_dir / "module_a.py").write_text("def foo():\n    pass")
        (self.src_dir / "module_b.py").write_text("class Bar:\n    pass")

    def teardown_method(self):
        shutil.rmtree(self.test_dir)

    def test_cache_creation_and_usage(self):
        analyzer = engine.ProjectAnalyzer(str(self.test_dir))

        # 1. First run (Cold Cache)
        results_1 = analyzer.collect()

        # Verify that modules were analyzed (they won't appear in most_complex_modules due to low complexity)
        assert len(results_1.get("modules", [])) == 2
        cache_file = self.test_dir / ".ai_context_cache.json"
        assert cache_file.exists()

        # Verify cache content
        cache_data = json.loads(cache_file.read_text())
        modules = {k: v for k, v in cache_data.items() if k != "_meta"}
        assert len(modules) == 2
        assert "src/module_a.py" in modules
        assert cache_data["_meta"]["schema"] == fs_utils.CACHE_SCHEMA

        # 2. Second run (Warm Cache)
        # Re-initialize to simulate fresh run ensuring it loads from disk
        analyzer_2 = engine.ProjectAnalyzer(str(self.test_dir))

        results_2 = analyzer_2.collect()

        # Ideally cached run is faster, but with 2 tiny files overhead might dominate.
        # So we check if results are identical.
        assert results_1["metrics"] == results_2["metrics"]

    def test_cache_invalidation(self):
        analyzer = engine.ProjectAnalyzer(str(self.test_dir))
        analyzer.collect()

        # Modify a file
        (self.src_dir / "module_a.py").write_text("def foo():\n    print('modified')")

        # Run again
        analyzer_2 = engine.ProjectAnalyzer(str(self.test_dir))
        analyzer_2.collect()

        # Check if modification was picked up (e.g. by checking hash in cache)
        cache_data = json.loads((self.test_dir / ".ai_context_cache.json").read_text())
        new_hash = fs_utils.calculate_file_hash(self.src_dir / "module_a.py")

        assert cache_data["src/module_a.py"]["hash"] == new_hash


class TestCacheVersioning:
    def setup_method(self):
        self.test_dir = pathlib.Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.test_dir)

    def _cache_file(self) -> pathlib.Path:
        return self.test_dir / ".ai_context_cache.json"

    def _read(self) -> dict:
        return json.loads(self._cache_file().read_text())

    def _write(self, data: dict) -> None:
        self._cache_file().write_text(json.dumps(data))

    def test_meta_written(self):
        fs_utils.save_cache(self.test_dir, {"a.py": {"data": 1}}, "fp-1")

        data = self._read()
        assert data["_meta"]["schema"] == fs_utils.CACHE_SCHEMA
        assert data["_meta"]["version"]
        assert data["_meta"]["config_fingerprint"] == "fp-1"
        assert data["a.py"] == {"data": 1}

    def test_load_requires_fingerprint_match(self):
        fs_utils.save_cache(self.test_dir, {"a.py": {"data": 1}}, "fp-1")

        assert fs_utils.load_cache(self.test_dir, "fp-2") == {}
        assert fs_utils.load_cache(self.test_dir, "fp-1") == {"a.py": {"data": 1}}

    def test_version_mismatch_invalidates(self):
        fs_utils.save_cache(self.test_dir, {"a.py": {"data": 1}}, "fp-1")
        data = self._read()
        data["_meta"]["version"] = "0.0.0"
        self._write(data)

        assert fs_utils.load_cache(self.test_dir, "fp-1") == {}

    def test_schema_mismatch_invalidates(self):
        fs_utils.save_cache(self.test_dir, {"a.py": {"data": 1}}, "fp-1")
        data = self._read()
        data["_meta"]["schema"] = 999
        self._write(data)

        assert fs_utils.load_cache(self.test_dir, "fp-1") == {}

    def test_legacy_cache_without_meta_is_ignored(self):
        self._write({"a.py": {"data": 1}})

        assert fs_utils.load_cache(self.test_dir, "fp-1") == {}

    def test_corrupt_cache_returns_empty(self):
        self._cache_file().write_text("{not json")

        assert fs_utils.load_cache(self.test_dir, "fp-1") == {}

    def test_config_fingerprint_is_stable_and_sensitive(self):
        assert fs_utils.compute_config_fingerprint({"a": 1}) == fs_utils.compute_config_fingerprint(
            {"a": 1}
        )
        assert fs_utils.compute_config_fingerprint({"a": 1}) != fs_utils.compute_config_fingerprint(
            {"a": 2}
        )
        assert fs_utils.compute_config_fingerprint(None) == fs_utils.compute_config_fingerprint({})
