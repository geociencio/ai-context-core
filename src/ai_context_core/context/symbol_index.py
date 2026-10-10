"""Versioned symbol index: definitions and references with ``file:line``."""

import ast
import json
import pathlib
from typing import Any, Dict, List, Optional, Tuple

from ..analyzer.providers import fs_utils

SCHEMA_VERSION = 1
SYMBOLS_FILE = "symbols.json"


def _collect_definitions(tree: ast.AST, rel: str) -> Tuple[List[Dict[str, Any]], set]:
    """Collect module/class/function/method definitions and their names."""
    definitions: List[Dict[str, Any]] = [{"name": rel, "kind": "module", "file": rel, "line": 1}]
    names: set = set()

    def visit(node: ast.AST, in_class: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                definitions.append(
                    {"name": child.name, "kind": "class", "file": rel, "line": child.lineno}
                )
                names.add(child.name)
                visit(child, True)
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                definitions.append(
                    {
                        "name": child.name,
                        "kind": "method" if in_class else "function",
                        "file": rel,
                        "line": child.lineno,
                    }
                )
                names.add(child.name)
                visit(child, in_class)
            else:
                visit(child, in_class)

    visit(tree, False)
    return definitions, names


def _collect_references(tree: ast.AST, rel: str, names: set) -> List[Dict[str, Any]]:
    """Collect load references to known defined names."""
    references: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in names:
            references.append({"name": node.id, "file": rel, "line": node.lineno})
    return references


def build_symbol_index(
    project_path: pathlib.Path, exclusion_patterns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Build a symbol index for the project.

    Args:
        project_path: Project root.
        exclusion_patterns: Extra ignore patterns; resolved from the project when
            omitted.

    Returns:
        A versioned index with ``symbols`` (definitions) and ``references``.
    """
    project_path = pathlib.Path(project_path).resolve()
    if exclusion_patterns is None:
        exclusion_patterns = fs_utils.load_exclusion_patterns(project_path, None)

    scan = fs_utils.scan_project(project_path, exclusion_patterns)
    trees: List[Tuple[str, ast.AST]] = []
    definitions: List[Dict[str, Any]] = []
    names: set = set()

    for file_path in scan.python_files:
        rel = str(file_path.relative_to(project_path))
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, SyntaxError):
            continue
        file_defs, file_names = _collect_definitions(tree, rel)
        definitions.extend(file_defs)
        names.update(file_names)
        trees.append((rel, tree))

    references: List[Dict[str, Any]] = []
    for rel, tree in trees:
        references.extend(_collect_references(tree, rel, names))

    definitions.sort(key=lambda d: (d["file"], d["line"]))
    references.sort(key=lambda r: (r["file"], r["line"], r["name"]))

    return {
        "schema": SCHEMA_VERSION,
        "symbols": definitions,
        "references": references,
    }


def write_symbol_index(project_path: pathlib.Path, index: Dict[str, Any]) -> pathlib.Path:
    """Write ``symbols.json`` and return its path."""
    target = pathlib.Path(project_path).resolve() / SYMBOLS_FILE
    with open(target, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False, default=str)
    return target


def load_symbol_index(project_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Load ``symbols.json`` if present, else ``None``."""
    target = pathlib.Path(project_path).resolve() / SYMBOLS_FILE
    if not target.exists():
        return None
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def search_symbols(index: Dict[str, Any], pattern: str) -> List[str]:
    """Return ``file:line`` matches for definitions and references.

    Args:
        index: A symbol index.
        pattern: Substring to match against symbol names.

    Returns:
        Newline-joined match strings: ``file:line: kind name`` for definitions
        and ``file:line: ref name`` for references.
    """
    needle = pattern.lower()
    matches: List[str] = []
    for sym in index.get("symbols", []):
        if needle in sym["name"].lower():
            matches.append(f"{sym['file']}:{sym['line']}: {sym['kind']} {sym['name']}")
    for ref in index.get("references", []):
        if needle in ref["name"].lower():
            matches.append(f"{ref['file']}:{ref['line']}: ref {ref['name']}")
    return matches
