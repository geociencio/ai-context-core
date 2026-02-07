"""Import extraction and unused detection visitor."""

import ast
from typing import List, Dict, Set

class ImportVisitor(ast.NodeVisitor):
    """Visitor to extract imports."""

    def __init__(self):
        """Initialize the ImportVisitor."""
        self.imports = []
        self.imported_names = {}  # alias_in_scope -> full_import_name
        self.used_names = set()

    def visit_Import(self, node: ast.Import):
        """Visits an import node."""
        for alias in node.names:
            self.imports.append(alias.name)
            name_in_scope = alias.asname or alias.name.split(".")[0]
            self.imported_names[name_in_scope] = alias.name

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Visits an import-from node."""
        module = node.module or ""
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports.append(full_name)
            name_in_scope = alias.asname or alias.name
            self.imported_names[name_in_scope] = full_name

    def visit_Name(self, node: ast.Name):
        """Visits a name node to track variable usage."""
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)

    def visit_Attribute(self, node: ast.Attribute):
        """Visits an attribute node to track variable usage."""
        curr = node.value
        while isinstance(curr, ast.Attribute):
            curr = curr.value
        if isinstance(curr, ast.Name):
            self.used_names.add(curr.id)
        self.generic_visit(node)

def extract_imports(tree: ast.AST) -> List[str]:
    """Extracts module imports from an AST tree."""
    visitor = ImportVisitor()
    visitor.visit(tree)
    return visitor.imports

def detect_unused_imports(tree: ast.AST) -> List[str]:
    """Identifies imports that are not used anywhere in the module."""
    visitor = ImportVisitor()
    visitor.visit(tree)

    unused = []
    for name_in_scope, full_import in visitor.imported_names.items():
        if name_in_scope not in visitor.used_names:
            unused.append(full_import)

    return unused
