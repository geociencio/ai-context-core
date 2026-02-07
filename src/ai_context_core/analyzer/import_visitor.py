"""Import analysis utilities for ai-context-core."""

import ast
from typing import List


from .import_visitor_components import (
    GenericImportVisitor as ImportVisitor,
    get_unique_imports,
    get_unused_imports
)

def extract_imports(tree: ast.AST) -> List[str]:
    """Extracts module imports in an optimized way.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of unique imports.
    """
    return get_unique_imports(tree)


def detect_unused_imports(tree: ast.AST) -> List[str]:
    """Identifies imports that are not used anywhere in the module.

    Args:
        tree: The AST tree to analyze.

    Returns:
        List of unused imports.
    """
    return get_unused_imports(tree)
