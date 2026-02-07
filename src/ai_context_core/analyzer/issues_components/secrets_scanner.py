"""Logic for scanning secrets in files."""

import pathlib
from typing import List, Dict, Any
from ..secrets import detect_secrets

def find_secrets(
    modules_data: List[Dict[str, Any]], project_path: str
) -> List[Dict[str, Any]]:
    """Scan project modules for exposed secrets."""
    res = []
    base = pathlib.Path(project_path)
    severities = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    
    for m in modules_data:
        path = m.get("path")
        if not path:
            continue
        try:
            with open(base / path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            issues_found = detect_secrets(content)
            if issues_found:
                max_sev_score = max(
                    (severities.get(i.get("severity", "low"), 0) for i in issues_found),
                    default=0,
                )
                max_sev_label = next(
                    (k for k, v in severities.items() if v == max_sev_score), "low"
                )

                res.append(
                    {
                        "module": path,
                        "issues": issues_found,
                        "total_issues": len(issues_found),
                        "max_severity": max_sev_label,
                    }
                )
        except Exception:
            continue
    return res
