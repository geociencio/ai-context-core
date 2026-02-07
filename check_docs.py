import ast
import os
from pathlib import Path


def check_docstrings(start_path):
    missing = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                        if not ast.get_docstring(tree):
                            missing.append(str(path))
                    except Exception:
                        pass
    return missing


if __name__ == "__main__":
    missing = check_docstrings("src/ai_context_core")
    for m in missing:
        print(m)
