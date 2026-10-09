"""AST visitor and helpers for extracting module imports."""

import ast
from typing import List, Optional
from .import_export import collect_exported_names


def get_package(path: str) -> str:
    """Derive the dotted package of a module's directory from its project-relative path.

    Args:
        path: Project-relative file path (e.g. ``core/x.py``).

    Returns:
        The dotted package of the containing directory (e.g. ``core``), or an
        empty string for a top-level module.
    """
    clean_path = path.replace("\\", "/")
    parts = clean_path.split("/")
    if parts and parts[0] == "src":
        parts = parts[1:]
    return ".".join(parts[:-1])


def _resolve_relative_package(package: str, level: int, module: str) -> str:
    """Resolve a relative import to an absolute dotted module prefix.

    Args:
        package: Dotted package of the source file's directory (e.g. ``core``).
        level: Relative import level (number of leading dots).
        module: The module part after the dots (may be empty).

    Returns:
        The absolute dotted prefix for the imported module.
    """
    parts = package.split(".") if package else []
    for _ in range(level - 1):
        parts = parts[:-1]
    base = ".".join(parts)
    if module:
        return f"{base}.{module}" if base else module
    return base


class ImportVisitor(ast.NodeVisitor):
    """Visitor to extract imports."""

    def __init__(self, package: Optional[str] = None):
        """Initialize the ImportVisitor.

        Args:
            package: Optional dotted package of the source module's directory,
                used to resolve relative imports (``node.level > 0``).
        """
        self.package = package
        self.imports = []
        self.imported_names = {}  # alias_in_scope -> full_import_name
        self.used_names = set()
        self.exported_names = set()  # names declared in __all__

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
            if node.level > 0 and self.package is not None:
                base = _resolve_relative_package(self.package, node.level, module)
                full_name = f"{base}.{alias.name}" if base else alias.name
            else:
                full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports.append(full_name)
            if module == "__future__":
                continue
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

    def visit_Assign(self, node: ast.Assign):
        """Tracks names exported via ``__all__ = [...]`` (re-export detection)."""
        self.exported_names |= collect_exported_names(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        """Tracks names appended via ``__all__ += [...]``."""
        self.exported_names |= collect_exported_names(node)
        self.generic_visit(node)


def extract_imports(tree: ast.AST, package: Optional[str] = None) -> List[str]:
    """Extracts module imports from an AST tree.

    Args:
        tree: The parsed AST tree.
        package: Optional dotted package of the source module's directory to
            resolve relative imports against.

    Returns:
        A list of absolute import strings.
    """
    visitor = ImportVisitor(package=package)
    visitor.visit(tree)
    return visitor.imports


def detect_unused_imports(tree: ast.AST) -> List[str]:
    """Identifies imports that are not used anywhere in the module.

    Names declared in ``__all__`` are treated as used, since assigning to
    ``__all__`` is the canonical way to re-export a module's public API.
    """
    visitor = ImportVisitor()
    visitor.visit(tree)

    unused = []
    for name_in_scope, full_import in visitor.imported_names.items():
        if name_in_scope in visitor.exported_names:
            continue
        if name_in_scope not in visitor.used_names:
            unused.append(full_import)

    return unused
