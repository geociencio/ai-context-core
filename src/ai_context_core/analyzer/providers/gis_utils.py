"""GIS specific filesystem utilities."""

import configparser
import pathlib
from typing import Dict, Any


def parse_metadata_content(content: str) -> Dict[str, str]:
    """Parse the raw text of a QGIS ``metadata.txt`` into a mapping.

    Args:
        content: Raw file content of a ``metadata.txt`` file.

    Returns:
        A dictionary of the parsed key/value pairs. Interpolation is disabled
        so literal ``%`` characters in values do not raise.
    """
    config = configparser.ConfigParser(strict=False, interpolation=None)
    config.read_string("[general]\n" + content.strip())
    return dict(config["general"]) if "general" in config else {}


def parse_qgis_metadata(project_path: pathlib.Path) -> Dict[str, Any]:
    metadata_file = project_path / "metadata.txt"
    res = {
        "exists": False,
        "valid": False,
        "content": {},
        "issues": [],
        "compliance_score": 0,
    }
    if not metadata_file.exists():
        res["issues"].append("Missing metadata.txt")
        return res
    res["exists"] = True
    try:
        content = metadata_file.read_text(encoding="utf-8")
        metadata = parse_metadata_content(content)
        res["content"] = metadata
        mandatory = [
            "name",
            "description",
            "version",
            "qgisminimumversion",
            "author",
            "email",
        ]
        for field in mandatory:
            if field not in metadata:
                res["issues"].append(f"Missing mandatory field: {field}")
        recommended = ["repository", "tracker", "homepage", "category", "tags"]
        for field in recommended:
            if field not in metadata:
                res["issues"].append(f"Missing recommended field: {field}")
        if not res["issues"]:
            res["valid"] = True
            res["compliance_score"] = 100
        else:
            res["compliance_score"] = max(0, 100 - (len(res["issues"]) * 10))
    except Exception as e:
        res["issues"].append(f"Error parsing metadata.txt: {str(e)}")
    return res
