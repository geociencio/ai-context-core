"""
Design patterns detection module for ai-context-core.
Uses AST to identify common architectural patterns.
"""

import ast
from typing import Dict, List, Any


def detect_patterns(tree: ast.AST) -> Dict[str, Any]:
    """
    Analyzes an AST to detect common design patterns.

    Args:
        tree: The AST to analyze.

    Returns:
        A dictionary containing detected patterns and their confidence levels.
    """
    patterns = {}

    # Singleton detection
    singleton_info = detect_singleton(tree)
    if singleton_info:
        patterns["Singleton"] = singleton_info

    # Factory detection
    factory_info = detect_factory(tree)
    if factory_info:
        patterns["Factory"] = factory_info

    # Observer detection
    observer_info = detect_observer(tree)
    if observer_info:
        patterns["Observer"] = observer_info

    # Strategy detection
    strategy_info = detect_strategy(tree)
    if strategy_info:
        patterns["Strategy"] = strategy_info

    # Decorator detection
    decorator_info = detect_decorator(tree)
    if decorator_info:
        patterns["Decorator"] = decorator_info

    return patterns


def detect_decorator(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects Decorator pattern implementations (wrappers).
    Looks for:
    1. Functions that define a 'wrapper' function inside and return it.
    2. Use of functools.wraps.
    3. Classes that take a callable in __init__ and implement __call__.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of detected Decorator patterns with confidence scores.
    """
    decorators = []

    for node in ast.walk(tree):
        # 1. Functional Decorators
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            confidence = 0
            evidence = []

            # Check for inner function that usually acts as a wrapper
            inner_func = None
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    inner_func = item
                    break

            if inner_func:
                # Check if it returns the inner function
                returns_inner = False
                for item in node.body:
                    if (
                        isinstance(item, ast.Return)
                        and isinstance(item.value, ast.Name)
                        and item.value.id == inner_func.name
                    ):
                        returns_inner = True
                        break

                if returns_inner:
                    evidence.append(
                        f"Function '{node.name}' contains and returns inner function '{inner_func.name}'"
                    )
                    confidence += 50

                    # Check for functools.wraps
                    for dec in inner_func.decorator_list:
                        if (
                            isinstance(dec, ast.Call)
                            and isinstance(dec.func, ast.Attribute)
                            and dec.func.attr == "wraps"
                        ) or (
                            isinstance(dec, ast.Call)
                            and isinstance(dec.func, ast.Name)
                            and dec.func.id == "wraps"
                        ):
                            evidence.append(
                                "Uses @functools.wraps on the inner function"
                            )
                            confidence += 40
                            break

            if confidence >= 50:
                decorators.append(
                    {
                        "name": node.name,
                        "type": "function",
                        "confidence": min(confidence, 100),
                        "evidence": evidence,
                    }
                )

        # 2. Class-based Decorators
        elif isinstance(node, ast.ClassDef):
            confidence = 0
            evidence = []

            has_init_callable = False
            has_call_method = False

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if item.name == "__init__":
                        # Check if it takes at least one arg (besides self) and stores it
                        if len(item.args.args) >= 2:
                            has_init_callable = True
                    elif item.name == "__call__":
                        has_call_method = True

            if has_init_callable and has_call_method:
                evidence.append(
                    "Class implements both __init__ (taking an object) and __call__"
                )
                confidence += 60

                if confidence >= 50:
                    decorators.append(
                        {
                            "name": node.name,
                            "type": "class",
                            "confidence": min(confidence, 100),
                            "evidence": evidence,
                        }
                    )

    return decorators


def detect_strategy(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects Strategy pattern implementations.
    Looks for:
    1. Context classes that accept a strategy/handler/engine object.
    2. Context classes that call a method on the stored strategy object.
    3. Naming conventions like '*Strategy', '*Algorithm'.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of detected Strategy patterns with confidence scores.
    """
    strategies = []

    # 1. Identify potential strategy implementations (classes/functions with specific names)
    potential_strategies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(
                kw in node.name.lower()
                for kw in ("strategy", "algorithm", "handler", "engine")
            ):
                potential_strategies.append(node.name)

    # 2. Look for Context classes using these strategies
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            confidence = 0
            evidence = []

            # Check for strategy injection in __init__ or setter
            has_injection = False
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and (
                    item.name == "__init__" or "set_" in item.name
                ):
                    for arg in item.args.args:
                        if any(
                            kw in arg.arg.lower()
                            for kw in (
                                "strategy",
                                "algorithm",
                                "engine",
                                "handler",
                                "mode",
                            )
                        ):
                            has_injection = True
                            evidence.append(
                                f"Strategy injection detected in '{item.name}' via argument '{arg.arg}'"
                            )
                            confidence += 30
                            # Try to find which attribute it's stored in
                            for sub in ast.walk(item):
                                if isinstance(sub, ast.Assign) and any(
                                    ast.unparse(t) == f"self.{arg.arg}"
                                    or arg.arg in ast.unparse(t)
                                    for t in sub.targets
                                ):
                                    break
                            break

            # Check for usage of stored strategy
            if has_injection:
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name not in (
                        "__init__",
                        "set_",
                    ):
                        for sub in ast.walk(item):
                            if isinstance(sub, ast.Call) and isinstance(
                                sub.func, ast.Attribute
                            ):
                                if any(
                                    kw in ast.unparse(sub.func).lower()
                                    for kw in (
                                        "strategy",
                                        "algorithm",
                                        "engine",
                                        "handler",
                                    )
                                ):
                                    evidence.append(
                                        f"Strategy call detected in method '{item.name}': {ast.unparse(sub.func)}()"
                                    )
                                    confidence += 40
                                    break

            if confidence >= 50:
                strategies.append(
                    {
                        "class": node.name,
                        "confidence": min(confidence, 100),
                        "evidence": evidence,
                    }
                )

    return strategies


def detect_observer(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects Observer pattern implementations.
    Looks for:
    1. Methods like attach/detach, subscribe/unsubscribe, notify.
    2. Collections of observers (list/set).
    3. Notification loops (for obs in observers: obs.update()).

    Args:
        tree: The AST to analyze.

    Returns:
        A list of detected Observer patterns with confidence scores.
    """
    observers = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            confidence = 0
            evidence = []

            # Check for observer collection initialization
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    for sub in ast.walk(item):
                        if isinstance(sub, ast.Assign):
                            for target in sub.targets:
                                if isinstance(target, ast.Attribute) and any(
                                    kw in target.attr.lower()
                                    for kw in ("observers", "subscribers", "listeners")
                                ):
                                    evidence.append(
                                        f"Observer collection '{target.attr}' initialized in __init__"
                                    )
                                    confidence += 20
                                    break

            # Check for attach/notify methods
            method_counts = 0
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m_name = item.name.lower()
                    if any(
                        kw in m_name
                        for kw in (
                            "attach",
                            "detach",
                            "subscribe",
                            "unsubscribe",
                            "register",
                            "unregister",
                        )
                    ):
                        method_counts += 1
                        evidence.append(f"Management method '{item.name}' detected")
                    if any(kw in m_name for kw in ("notify", "emit", "broadcast")):
                        method_counts += 1
                        evidence.append(f"Notification method '{item.name}' detected")

                        # Look for loop over collection inside notify
                        for sub in ast.walk(item):
                            if isinstance(sub, ast.For) and any(
                                kw in ast.unparse(sub.iter).lower()
                                for kw in ("observers", "subscribers", "listeners")
                            ):
                                confidence += 30
                                evidence.append(
                                    "Notification method contains a loop over the observer collection"
                                )
                                break

            confidence += method_counts * 15

            if confidence >= 50:
                observers.append(
                    {
                        "class": node.name,
                        "confidence": min(confidence, 100),
                        "evidence": evidence,
                    }
                )

    return observers


def detect_factory(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects Factory pattern implementations.
    Looks for:
    1. Methods named create_*, build_*, get_*, or factory.
    2. Methods that instantiate and return objects.
    3. Static or class methods in a "Factory" named class.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of detected Factory patterns with confidence scores.
    """
    factories = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check class name
            class_confidence = 0
            if "factory" in node.name.lower():
                class_confidence += 30

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    confidence = class_confidence
                    evidence = []

                    if class_confidence > 0:
                        evidence.append(
                            f"Class '{node.name}' contains 'Factory' in its name"
                        )

                    # Check method name
                    method_name = item.name.lower()
                    if any(
                        prefix in method_name
                        for prefix in ("create_", "build_", "make_", "factory")
                    ):
                        confidence += 40
                        evidence.append(
                            f"Method '{item.name}' matches common factory naming conventions"
                        )

                    # Check if it returns an instantiation
                    for subnode in ast.walk(item):
                        if isinstance(subnode, ast.Return) and isinstance(
                            subnode.value, ast.Call
                        ):
                            # Simple check: returns something initialized
                            confidence += 30
                            evidence.append(
                                "Method contains a return statement that instantiates a class"
                            )
                            break

                    if confidence >= 60:
                        factories.append(
                            {
                                "class": node.name,
                                "method": item.name,
                                "confidence": min(confidence, 100),
                                "evidence": evidence,
                            }
                        )

    return factories


def detect_singleton(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects Singleton pattern implementations.
    Looks for:
    1. A class with a private instance (e.g., _instance = None)
    2. A class method or static method that returns the instance (e.g., get_instance())
    3. Overriding __new__ to control instantiation.

    Args:
        tree: The AST to analyze.

    Returns:
        A list of detected Singleton patterns with confidence scores.
    """
    singletons = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            confidence = 0
            evidence = []

            # 1. Check for __new__ override (Strongest indicator)
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__new__":
                    evidence.append("Overrides __new__ to control instantiation")
                    confidence += 60
                    break

            # 2. Check for class methods like "get_instance" or similar
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Check decorators for @classmethod or @staticmethod
                    is_class_or_static = any(
                        (
                            isinstance(dec, ast.Name)
                            and dec.id in ("classmethod", "staticmethod")
                        )
                        or (
                            isinstance(dec, ast.Attribute)
                            and dec.attr in ("classmethod", "staticmethod")
                        )
                        for dec in item.decorator_list
                    )

                    if is_class_or_static and any(
                        keyword in item.name.lower()
                        for keyword in ("instance", "singleton", "get_inst")
                    ):
                        evidence.append(f"Static/Class method '{item.name}' detected")
                        confidence += 30

            # 3. Check for static instance variable
            for item in node.body:
                if isinstance(item, (ast.Assign, ast.AnnAssign)):
                    targets = (
                        item.targets if isinstance(item, ast.Assign) else [item.target]
                    )
                    for target in targets:
                        if isinstance(target, ast.Name) and any(
                            keyword in target.id.lower()
                            for keyword in ("instance", "_inst")
                        ):
                            evidence.append(
                                f"Static instance variable '{target.id}' found"
                            )
                            confidence += 20

            if confidence >= 50:
                singletons.append(
                    {
                        "class": node.name,
                        "confidence": min(confidence, 100),
                        "evidence": evidence,
                    }
                )

    return singletons
