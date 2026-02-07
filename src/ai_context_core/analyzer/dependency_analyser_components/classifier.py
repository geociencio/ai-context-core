"""Logic for classifying imports into internal, external, and third-party."""

from typing import Dict, List, Set

def classify_imports(all_imports: Set[str], stdlib_modules: Set[str], known_internal: Set[str] = None) -> Dict[str, List[str]]:
    """Categorizes imports into internal, external (StdLib), and third-party modules."""
    results = {"internal": [], "external": [], "third_party": []}
    known_internal = known_internal or set()

    for imp in sorted(all_imports):
        root_pkg = imp.split(".")[0]
        is_known_internal = False
        if imp in known_internal:
            is_known_internal = True
        else:
            for internal in known_internal:
                if imp == internal or imp.startswith(internal + "."):
                    is_known_internal = True
                    break

        if is_known_internal or imp.startswith(".") or any(seg in imp for seg in ["..", "./"]):
            results["internal"].append(imp)
        elif root_pkg in stdlib_modules:
            results["external"].append(imp)
        else:
            results["third_party"].append(imp)

    return results
