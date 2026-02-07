"""Logic for updating context update files."""

import yaml
import pathlib
from typing import Dict, Any

def update_context_file(project_path: pathlib.Path, info: Dict[str, Any]) -> None:
    """Updates the .ai-context-updates.yaml file with new information."""
    p = project_path / ".ai-context-updates.yaml"
    cur = _load_current_updates(p)
    
    for k, v in info.items():
        if k in cur and isinstance(cur[k], dict) and isinstance(v, dict):
            cur[k].update(v)
        elif k in cur and isinstance(cur[k], list) and isinstance(v, list):
            cur[k].extend(v)
        else:
            cur[k] = v

    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(cur, f)

def _load_current_updates(p: pathlib.Path) -> Dict[str, Any]:
    """Helper to load existing update file."""
    if p.exists():
        try:
            return yaml.safe_load(p.read_text()) or {}
        except Exception:
            pass
    return {}
