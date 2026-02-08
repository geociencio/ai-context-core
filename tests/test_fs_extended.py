import pathlib
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.providers.fs_scanner import ProjectScanner
from ai_context_core.analyzer.providers.fs_tree import (
    generate_tree_optimized,
    _generate_tree_fallback,
)
from ai_context_core.analyzer.providers.fs_cache import load_cache, save_cache, LRUCache


def test_fs_scanner_getsize_oserror():
    # Coverage for fs_scanner.py line 84-85
    with patch("os.path.getsize", side_effect=OSError("Permission denied")):
        scanner = ProjectScanner(pathlib.Path("/tmp"), MagicMock())
        # We need a file to process
        scanner._process_file("/tmp", "", "test.py")
        assert scanner.stats["total_size"] == 0


def test_fs_scanner_finalize_empty():
    # Coverage for fs_scanner.py line 115-117 (tf=0 or ts=0)
    scanner = ProjectScanner(pathlib.Path("/tmp"), MagicMock())
    res = scanner._finalize_stats()
    assert res["avg_file_size_kb"] == 0
    assert res["python_percentage"] == 0


def test_fs_tree_optimized_exception():
    # Coverage for fs_tree.py line 29-30
    with patch("subprocess.run", side_effect=Exception("Subprocess failed")):
        # Should fallback to manual generation
        with patch(
            "ai_context_core.analyzer.providers.fs_tree._generate_tree_fallback"
        ) as mock_fallback:
            generate_tree_optimized(pathlib.Path("/tmp"))
            mock_fallback.assert_called()


def test_fs_tree_fallback_more_files():
    # Coverage for fs_tree.py line 47-49 (... +N more)
    with patch("os.walk") as mock_walk:
        # Mock walk returns 11 files to ensure (+3 more)
        mock_walk.return_value = [
            (
                "/tmp",
                ["subdir"],
                ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"],
            )
        ]
        res = _generate_tree_fallback(pathlib.Path("/tmp"))
        assert "(+3 more)" in res


def test_fs_cache_load_exception():
    # Coverage for fs_cache.py line 41-42
    with patch("builtins.open", side_effect=Exception("Read error")):
        with patch("pathlib.Path.exists", return_value=True):
            assert load_cache(pathlib.Path("/tmp")) == {}


def test_fs_cache_save_exception():
    # Coverage for fs_cache.py line 50-51
    with patch("builtins.open", side_effect=Exception("Write error")):
        # Should not raise
        save_cache(pathlib.Path("/tmp"), {"data": 1})


def test_lru_cache_clear():
    # Coverage for LRUCache.clear (line 27-28)
    cache = LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.clear()
    assert cache.get("a") is None
    assert len(cache.cache) == 0


def test_lru_cache_move_to_end_on_set():
    # Coverage for LRUCache.set move_to_end (line 21-22)
    cache = LRUCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("a", 10)  # a is moved to end
    cache.set("c", 3)  # b (the oldest) should be evicted
    assert cache.get("b") is None
    assert cache.get("a") == 10
    assert cache.get("c") == 3
