"""Project structure visualization."""

import os
import pathlib
import subprocess
from typing import Dict, Any


def generate_tree_optimized(project_path: pathlib.Path) -> str:
    try:
        result = subprocess.run(
            [
                "tree",
                "-I",
                "__pycache__|*.pyc|*.pyo|*.pycache|.git|.venv|venv|env",
                "-a",
                "--noreport",
                "-L",
                "4",
            ],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout[:1500]
    except Exception:
        pass
    return _generate_tree_fallback(project_path)


def _generate_tree_fallback(project_path: pathlib.Path) -> str:
    tree_lines = ["./"]
    for root, dirs, files in os.walk(project_path):
        depth = root[len(str(project_path)) :].count(os.sep)
        if depth > 4:
            continue
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        indent = "    " * depth
        rel_root = os.path.relpath(root, project_path)
        if rel_root != ".":
            tree_lines.append(f"{indent}{os.path.basename(root)}/")
        f_indent = "    " * (depth + 1)
        for i, file in enumerate(sorted(files)[:8]):
            if i == 7 and len(files) > 8:
                tree_lines.append(f"{f_indent}... (+{len(files) - 8} more)")
                break
            tree_lines.append(f"{f_indent}{file}")
    return "\n".join(tree_lines)


def analyze_structure(project_path: pathlib.Path, modules_count: int) -> Dict[str, Any]:
    from .fs_scanner import scan_project

    res = scan_project(project_path, [])
    return {
        "tree": generate_tree_optimized(project_path),
        "modules_count": modules_count,
        "file_types": res.file_types,
        "size_stats": res.size_stats,
    }
