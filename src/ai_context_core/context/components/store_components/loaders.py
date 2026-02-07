"""Logic for loading context files of various formats."""

import json
import yaml
import pathlib
from typing import Dict, Any, List


def load_context_files(
    project_path: pathlib.Path, file_list: List[str]
) -> Dict[str, Any]:
    """Loads all relevant context files from the project path."""
    res = {}
    for f in file_list:
        p = project_path / f
        if p.exists():
            res[f] = load_single_context_file(p)
    return res


def load_single_context_file(p: pathlib.Path) -> Any:
    """Loads a single context file based on extension (json, yaml, md)."""
    try:
        if p.suffix == ".json":
            return json.loads(p.read_text(encoding="utf-8"))
        if p.suffix in (".yaml", ".yml"):
            return yaml.safe_load(p.read_text(encoding="utf-8"))
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""
