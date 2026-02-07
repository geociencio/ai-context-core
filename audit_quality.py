import json
from pathlib import Path


def audit():
    if not Path("project_context.json").exists():
        print("project_context.json not found")
        return

    with open("project_context.json", "r") as f:
        data = json.load(f)

    modules = data.get("modules", [])
    print(f"Total modules: {len(modules)}")

    # 1. Low MSI
    low_msi = [m for m in modules if m.get("maintenance_index", 100) < 60]
    print(f"\nModules with MSI < 60: {len(low_msi)}")
    for m in sorted(low_msi, key=lambda x: x.get("maintenance_index", 100)):
        print(
            f"  - {m['path']}: {m.get('maintenance_index'):.1f} (C:{m.get('complexity')}, S:{m.get('sloc')})"
        )

    # 2. High Complexity (>10)
    high_comp = [m for m in modules if m.get("complexity", 0) > 10]
    print(f"\nModules with Complexity > 10: {len(high_comp)}")
    for m in sorted(high_comp, key=lambda x: x.get("complexity", 0), reverse=True):
        print(
            f"  - {m['path']}: {m.get('complexity')} (MSI:{m.get('maintenance_index', 0):.1f})"
        )


if __name__ == "__main__":
    audit()
