"""AST utilities for Python code analysis.

This module provides tools for extracting functions, classes, complexity,
type hint coverage, Halstead metrics, and imports from Python source code.
"""

import ast
from collections import Counter
from typing import Any, List, Dict


HALSTEAD_OPERATORS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.FloorDiv,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Invert,
    ast.UAdd,
    ast.USub,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
    ast.FunctionDef,
    ast.ClassDef,
)


def extract_functions(tree: ast.AST) -> List[str]:
    """Extracts function names and basic argument counts from an AST.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of strings representing function names and their argument counts (e.g., "func(3 args)").
    """
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = node.name
            # Extract arguments
            args_count = len(node.args.args)
            if args_count > 0:
                func_info = f"{func_info}({args_count} args)"
            functions.append(func_info)
    return functions


def extract_classes(tree: ast.AST) -> List[str]:
    """Extracts class names with inheritance information from an AST.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of strings representing class names and their bases (e.g., "ClassName(BaseClass)").
    """
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Include inheritance info
            bases = [get_base_name(base) for base in node.bases]
            inheritance = f"({', '.join(bases)})" if bases else ""
            classes.append(f"{node.name}{inheritance}")
    return classes


def get_base_name(node: ast.AST) -> str:
    """Retrieves the name of a base class from an AST node.

    Args:
        node: The AST node representing the base class.

    Returns:
        The name of the base class as a string, or "Unknown" if it cannot be determined.
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return ast.unparse(node)
    return "Unknown"


def check_docstrings(tree: ast.AST) -> Dict[str, Any]:
    """Checks for the presence of docstrings in modules, classes, and functions.

    Args:
        tree: The AST to analyze.

    Returns:
        A dictionary containing boolean values for module docstring presence and
        nested dictionaries for classes and functions.
    """
    docstrings = {"module": False, "classes": {}, "functions": {}}

    # Module docstring
    if isinstance(tree, ast.Module):
        docstrings["module"] = ast.get_docstring(tree) is not None

    # Class and function docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstrings["classes"][node.name] = ast.get_docstring(node) is not None
        elif isinstance(node, ast.FunctionDef):
            docstrings["functions"][node.name] = ast.get_docstring(node) is not None

    return docstrings


def is_entry_point(tree: ast.AST) -> Dict[str, Any]:
    """Determines if the module is an entry point.

    Checks for:
    - Standard main guard: if __name__ == "__main__"
    - QGIS Plugin: classFactory(iface) function
    - Click CLI: @click.command decorator
    - Flask/FastAPI: Route decorators (@app.route, @app.get, etc)

    Args:
        tree: The AST to analyze.

    Returns:
        A dictionary with 'is_entry_point' (bool) and 'type' (str or None).
    """
    result = {"is_entry_point": False, "type": None}

    for node in ast.walk(tree):
        # 1. Standard main guard
        if isinstance(node, ast.If):
            try:
                if (
                    isinstance(node.test, ast.Compare)
                    and isinstance(node.test.left, ast.Name)
                    and node.test.left.id == "__name__"
                ):
                    for comparator in node.test.comparators:
                        if (
                            isinstance(comparator, ast.Constant)
                            and comparator.value == "__main__"
                        ):
                            return {"is_entry_point": True, "type": "main_guard"}
            except Exception:
                pass

        # 2. Function definitions (QGIS)
        if isinstance(node, ast.FunctionDef):
            # QGIS classFactory
            if node.name == "classFactory" and any(
                arg.arg == "iface" for arg in node.args.args
            ):
                return {"is_entry_point": True, "type": "qgis_plugin"}

            # Decorators (Click, Flask, FastAPI)
            for decorator in node.decorator_list:
                # Normalize decorator to the attribute/name being used
                # e.g. @click.command -> Attribute
                # e.g. @click.command() -> Call -> func is Attribute

                check_node = decorator
                if isinstance(decorator, ast.Call):
                    check_node = decorator.func

                # Check for Attribute (e.g. click.command, app.route)
                if isinstance(check_node, ast.Attribute):
                    # Click: @click.command or @click.group
                    if (
                        isinstance(check_node.value, ast.Name)
                        and check_node.value.id == "click"
                    ):
                        if check_node.attr in ("command", "group"):
                            return {"is_entry_point": True, "type": "click_cli"}

                    # Flask: @app.route
                    if check_node.attr == "route":
                        return {"is_entry_point": True, "type": "flask_app"}

                    # FastAPI: @app.get, @app.post, etc. (common HTTP verbs)
                    if check_node.attr in ("get", "post", "put", "delete", "patch"):
                        return {"is_entry_point": True, "type": "fastapi_app"}

                # Check for Name (e.g. @cli, if cli is a Click group? Hard to know without context)
                # But typically Click uses decorators on functions.
                # Use specific known names if needed, but 'click.command' is standard.

    return result


def has_main_guard(tree: ast.AST) -> bool:
    """Checks if the module contains the standard 'if __name__ == "__main__":' guard.

    Deprecated: Use is_entry_point() instead.

    Args:
        tree: The AST to analyze.

    Returns:
        True if the guard is found, False otherwise.
    """
    result = is_entry_point(tree)
    return result["is_entry_point"] and result["type"] == "main_guard"


def calculate_type_hint_coverage(tree: ast.AST) -> Dict[str, Any]:
    """Calculates the percentage of functions with type hints.

    Args:
        tree: The AST to analyze.

    Returns:
        A dictionary with total_functions, typed_functions, and coverage percentage.
    """
    total_items = 0
    typed_items = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            total_items += 1
            # Check return type
            has_return_type = node.returns is not None

            # Check arguments (excluding self/cls)
            args = [arg for arg in node.args.args if arg.arg not in ("self", "cls")]
            total_args = len(args)
            typed_args = sum(1 for arg in args if arg.annotation is not None)

            if has_return_type and (total_args == 0 or total_args == typed_args):
                typed_items += 1

    return {
        "total_functions": total_items,
        "typed_functions": typed_items,
        "coverage": (typed_items / total_items * 100) if total_items > 0 else 100.0,
    }


def calculate_halstead_metrics(tree: ast.AST) -> Dict[str, Any]:
    """Calculates basic Halstead complexity metrics.

    Args:
        tree: The AST to analyze.

    Returns:
        A dictionary containing vocabulary, length, volume, difficulty, and effort.
    """
    operators = Counter()
    operands = Counter()

    for node in ast.walk(tree):
        node_type = type(node).__name__
        if isinstance(node, HALSTEAD_OPERATORS):
            operators[node_type] += 1
        elif isinstance(node, ast.Name):
            operands[node.id] += 1
        elif isinstance(node, ast.Constant):
            operands[str(node.value)] += 1

    n1 = len(operators)  # unique operators
    n2 = len(operands)  # unique operands
    N1 = sum(operators.values())  # total operators
    N2 = sum(operands.values())  # total operands

    h_vocabulary = n1 + n2
    h_length = N1 + N2

    if n1 > 0 and n2 > 0:
        h_volume = h_length * (h_vocabulary.bit_length() - 1)
        h_difficulty = (n1 / 2) * (N2 / n2)
        h_effort = h_difficulty * h_volume
    else:
        h_volume = h_difficulty = h_effort = 0

    return {
        "vocabulary": h_vocabulary,
        "length": h_length,
        "volume": round(h_volume, 2),
        "difficulty": round(h_difficulty, 2),
        "effort": round(h_effort, 2),
    }


def extract_imports(tree: ast.AST) -> List[str]:
    """Extracts module imports in an optimized way.

    Args:
        tree: The AST to analyze.

    Returns:
        A unique list of imported module names.
    """
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if module:
                    imports.append(f"{module}.{alias.name}")
                else:
                    imports.append(alias.name)

    # De-duplicate while maintaining order
    seen = set()
    unique_imports = []
    for imp in imports:
        if imp not in seen:
            seen.add(imp)
            unique_imports.append(imp)

    return unique_imports


def calculate_complexity(tree: ast.AST) -> int:
    """Calculates optimized cyclomatic complexity.

    Args:
        tree: The AST to analyze.

    Returns:
        The calculated cyclomatic complexity as an integer.
    """
    complexity = 0
    decision_lines = set()

    for node in ast.walk(tree):
        # Decision nodes
        if isinstance(
            node,
            (
                ast.If,
                ast.While,
                ast.For,
                ast.Try,
                ast.ExceptHandler,
                ast.AsyncFor,
                ast.AsyncWith,
            ),
        ):
            complexity += 1
            if hasattr(node, "lineno"):
                decision_lines.add(node.lineno)

        # Boolean operators
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1

        # Comprehensions
        elif isinstance(
            node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            complexity += len(node.generators)

    # Penalty for highly dense logic (many decisions in few lines)
    if decision_lines:
        density = len(decision_lines) / (max(decision_lines) - min(decision_lines) + 1)
        if density > 0.5:
            complexity = int(complexity * 1.2)

    return complexity
