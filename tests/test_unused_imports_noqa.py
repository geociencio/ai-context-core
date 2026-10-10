"""``# noqa`` opt-out for unused-import detection (v5.1.0, WS-6)."""

import ast

from ai_context_core.analyzer.visitors.imports_visitor import (
    detect_unused_imports,
    find_noqa_lines,
)


def _tree(src: str) -> ast.AST:
    return ast.parse(src)


def test_unused_import_detected_without_content():
    src = "from .cycle_detector import CycleDetector\nx = 1\n"
    assert detect_unused_imports(_tree(src)) == ["cycle_detector.CycleDetector"]


def test_bare_noqa_suppresses():
    src = "from .cycle_detector import CycleDetector  # noqa\nx = 1\n"
    assert detect_unused_imports(_tree(src), src) == []


def test_noqa_f401_suppresses():
    src = "from .cycle_detector import CycleDetector  # noqa: F401\nx = 1\n"
    assert detect_unused_imports(_tree(src), src) == []


def test_noqa_other_code_does_not_suppress_f401():
    src = "from .cycle_detector import CycleDetector  # noqa: E501\nx = 1\n"
    assert detect_unused_imports(_tree(src), src) == ["cycle_detector.CycleDetector"]


def test_multiline_import_noqa_on_spanning_line():
    src = "from .pkg import (\n    Thing,  # noqa: F401\n)\n"
    assert detect_unused_imports(_tree(src), src) == []


def test_used_import_not_reported():
    src = "from .cycle_detector import CycleDetector\nprint(CycleDetector)\n"
    assert detect_unused_imports(_tree(src), src) == []


def test_find_noqa_lines_codes():
    src = "a = 1  # noqa: F401, E501\nb = 2  # noqa\nc = 3  # noqa: E501\n"
    assert find_noqa_lines(src) == {1, 2}
