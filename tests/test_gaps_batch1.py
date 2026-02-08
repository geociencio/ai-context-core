"""
Tests para cubrir gaps en fs_helpers, complexity_visitor y otros módulos core.
"""

import pathlib
from unittest.mock import patch, MagicMock, mock_open
from ai_context_core.analyzer.providers.fs_helpers import (
    read_file_fast,
    calculate_file_hash,
)
from ai_context_core.analyzer.visitors.complexity_visitor import (
    ComplexityVisitor,
    _apply_complexity_penalty,
)
import ast


def test_read_file_fast_not_exists():
    # Coverage for fs_helpers.py line 19
    with patch("pathlib.Path.exists", return_value=False):
        result = read_file_fast(pathlib.Path("/fake/path.py"))
        assert result == ""


def test_read_file_fast_large_file_mmap():
    # Coverage for fs_helpers.py lines 23-24 (mmap for large files)
    fake_content = b"x" * (2 * 1024 * 1024)  # 2MB file

    with patch("pathlib.Path.exists", return_value=True):
        with patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = len(fake_content)
            with patch("builtins.open", mock_open(read_data=fake_content)):
                with patch("mmap.mmap") as mock_mmap:
                    mock_mm = MagicMock()
                    mock_mm.read.return_value = fake_content
                    mock_mm.__enter__.return_value = mock_mm
                    mock_mmap.return_value = mock_mm

                    result = read_file_fast(pathlib.Path("/large/file.py"))
                    assert len(result) > 0


def test_read_file_fast_exception():
    # Coverage for fs_helpers.py lines 29-30
    with patch("pathlib.Path.exists", side_effect=Exception("Read error")):
        result = read_file_fast(pathlib.Path("/error/file.py"))
        assert result == ""


def test_calculate_file_hash_empty_content():
    # Coverage for fs_helpers.py lines 47, 49-50
    with patch(
        "ai_context_core.analyzer.providers.fs_helpers.read_file_fast", return_value=""
    ):
        result = calculate_file_hash(pathlib.Path("/empty.py"))
        assert result == ""

    with patch(
        "ai_context_core.analyzer.providers.fs_helpers.read_file_fast",
        side_effect=Exception("Hash error"),
    ):
        result = calculate_file_hash(pathlib.Path("/error.py"))
        assert result == ""


def test_complexity_visitor_match_case():
    # Coverage for complexity_visitor.py lines 40-41 (Match/MatchCase)
    code = """
match value:
    case 1:
        pass
    case 2:
        pass
"""
    try:
        tree = ast.parse(code)
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        # Match statements add complexity (1 for Match node)
        assert visitor.complexity >= 1
    except SyntaxError:
        # Python < 3.10 doesn't support match
        pass


def test_complexity_visitor_async_with():
    # Coverage for complexity_visitor.py lines 49-50 (AsyncWith)
    code = """
async def foo():
    async with context:
        pass
"""
    tree = ast.parse(code)
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    assert visitor.complexity >= 1


def test_complexity_penalty_no_penalty():
    # Coverage for complexity_visitor.py line 167
    # When decision_lines is empty, no penalty
    result = _apply_complexity_penalty(5, [])
    assert result == 5
