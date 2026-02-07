"""Class extraction visitor."""

import ast
from typing import List, Optional

class ClassVisitor(ast.NodeVisitor):
    """Visitor to extract class names and inheritance infomation."""

    def __init__(self):
        """Initialize the ClassVisitor."""
        self.classes = []

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits a class definition and extracts inheritance."""
        bases = [self._get_base_name(base) for base in node.bases]
        inheritance = f"({', '.join(bases)})" if bases else ""
        self.classes.append(f"{node.name}{inheritance}")
        self.generic_visit(node)

    def _get_base_name(self, node: ast.AST) -> Optional[str]:
        """Extracts the base name from a Name or Attribute node."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return self._get_base_name(node.value)
        return None

def extract_classes(tree: ast.AST) -> List[str]:
    """Extracts class names with inheritance information from an AST."""
    visitor = ClassVisitor()
    visitor.visit(tree)
    return visitor.classes
