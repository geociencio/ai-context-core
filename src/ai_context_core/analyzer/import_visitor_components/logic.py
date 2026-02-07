"""Logic for import extraction and unused detection."""

import ast
from typing import List
from .visitor import GenericImportVisitor


def get_unique_imports(tree: ast.AST) -> List[str]:
    """Extracts module imports and de-duplicates them."""
    visitor = GenericImportVisitor()
    visitor.visit(tree)

    seen = set()
    unique_imports = []
    for imp in visitor.imports:
        if imp not in seen:
            seen.add(imp)
            unique_imports.append(imp)
    return unique_imports


def get_unused_imports(tree: ast.AST) -> List[str]:
    """Identifies imports that are not used anywhere in the module."""
    visitor = GenericImportVisitor()
    visitor.visit(tree)

    unused = [
        name
        for alias, name in visitor.imported_names.items()
        if alias not in visitor.used_names and alias != "*"
    ]
    return sorted(list(set(unused)))
