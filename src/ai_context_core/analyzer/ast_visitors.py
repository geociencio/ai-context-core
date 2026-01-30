"""Generic AST visitors for information extraction."""

import ast
from typing import List, Dict, Any


class FunctionVisitor(ast.NodeVisitor):
    """Visitor to extract function names and argument counts."""

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_info = node.name
        args_count = len(node.args.args)
        if args_count > 0:
            func_info = f"{func_info}({args_count} args)"
        self.functions.append(func_info)
        self.generic_visit(node)


class ClassVisitor(ast.NodeVisitor):
    """Visitor to extract class names and inheritance infomation."""

    def __init__(self):
        self.classes = []

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [self._get_base_name(base) for base in node.bases]
        inheritance = f"({', '.join(bases)})" if bases else ""
        self.classes.append(f"{node.name}{inheritance}")
        self.generic_visit(node)

    def _get_base_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return ast.unparse(node)
        return "Unknown"


class DocstringVisitor(ast.NodeVisitor):
    """Visitor to check for docstring presence."""

    def __init__(self):
        self.docstrings = {"module": False, "classes": {}, "functions": {}}

    def visit_Module(self, node: ast.Module):
        self.docstrings["module"] = ast.get_docstring(node) is not None
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.docstrings["classes"][node.name] = ast.get_docstring(node) is not None
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.docstrings["functions"][node.name] = ast.get_docstring(node) is not None
        self.generic_visit(node)


class ImportVisitor(ast.NodeVisitor):
    """Visitor to extract imports."""

    def __init__(self):
        self.imports = []
        self.imported_names = {}  # alias_in_scope -> full_import_name
        self.used_names = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
            name_in_scope = alias.asname or alias.name.split(".")[0]
            self.imported_names[name_in_scope] = alias.name

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            if module:
                full_name = f"{module}.{alias.name}"
                self.imports.append(full_name)
            else:
                full_name = alias.name
                self.imports.append(full_name)

            name_in_scope = alias.asname or alias.name
            self.imported_names[name_in_scope] = full_name

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)

    def visit_Attribute(self, node: ast.Attribute):
        # Recursively find the base Name in an Attribute chain (e.g., a.b.c)
        curr = node.value
        while isinstance(curr, ast.Attribute):
            curr = curr.value
        if isinstance(curr, ast.Name):
            self.used_names.add(curr.id)
        self.generic_visit(node)


def extract_functions(tree: ast.AST) -> List[str]:
    """Extracts function names and basic argument counts from an AST."""
    visitor = FunctionVisitor()
    visitor.visit(tree)
    return visitor.functions


def extract_classes(tree: ast.AST) -> List[str]:
    """Extracts class names with inheritance information from an AST."""
    visitor = ClassVisitor()
    visitor.visit(tree)
    return visitor.classes


def check_docstrings(tree: ast.AST) -> Dict[str, Any]:
    """Checks for the presence of docstrings in modules, classes, and functions."""
    visitor = DocstringVisitor()
    visitor.visit(tree)
    return visitor.docstrings


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
