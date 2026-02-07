"""Rules for identifying observer pattern evidence."""

import ast

# --- Collection Rules ---

KEYWORDS_INIT = ("observers", "subscribers", "listeners")
KEYWORDS_MGMT = (
    "attach",
    "detach",
    "subscribe",
    "unsubscribe",
    "register",
    "unregister",
)
KEYWORDS_NOTIFY = ("notify", "emit", "broadcast")


def check_init_assign(node: ast.Assign) -> bool:
    """Check if assignment is for an observer collection."""
    for t in node.targets:
        if isinstance(t, ast.Attribute) and any(
            kw in t.attr.lower() for kw in KEYWORDS_INIT
        ):
            return True
    return False


def check_iteration(node: ast.AST) -> bool:
    """Check for iteration over observer collections."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.For):
            iter_str = ast.unparse(sub.iter).lower()
            if any(kw in iter_str for kw in KEYWORDS_INIT):
                return True
    return False


def check_mgmt_method(name: str) -> bool:
    """Check if method name matches management patterns."""
    m_low = name.lower()
    return any(kw in m_low for kw in KEYWORDS_MGMT)


def check_notify_method(name: str) -> bool:
    """Check if method name matches notification patterns."""
    m_low = name.lower()
    return any(kw in m_low for kw in KEYWORDS_NOTIFY)


# --- Signal Rules ---


def detect_signals(node: ast.AST) -> int:
    """Count signal definitions in a node."""
    signals_found = 0
    for item in ast.iter_child_nodes(node):
        if _is_signal_definition(item):
            signals_found += 1
    return signals_found


def _is_signal_definition(node: ast.AST) -> bool:
    """Determine if an AST node defines a signal."""
    if not isinstance(node, (ast.Assign, ast.AnnAssign)):
        return False

    val = node.value
    if not (val and isinstance(val, ast.Call)):
        return False

    try:
        func_str = ast.unparse(val.func).lower()
        return "pyqtsignal" in func_str or "signal" in func_str
    except Exception:
        return False


# --- Class Analysis Rules ---


def analyze_class_body(node: ast.ClassDef, add_evidence_func) -> None:
    """Analyze class body for observer patterns."""
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            _check_init(item, add_evidence_func)
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_method(item, add_evidence_func)


def _check_init(node: ast.FunctionDef, add_evidence_func) -> None:
    """Check __init__ for observer collection initialization."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Assign) and check_init_assign(sub):
            add_evidence_func("Observer collection initialized in __init__", 20)

        if isinstance(sub, ast.Call):
            _check_connection_call(sub, add_evidence_func)


def _check_connection_call(node: ast.Call, add_evidence_func) -> None:
    """Check if a call node is a signal connection."""
    try:
        func_name = ast.unparse(node.func).lower()
        if ".connect" in func_name:
            add_evidence_func(f"Signal connection detected: {func_name}", 10)
    except Exception:
        pass


def _check_method(node: ast.FunctionDef, add_evidence_func) -> None:
    """Check a method for observer management or notification."""
    if check_mgmt_method(node.name):
        add_evidence_func(f"Management method '{node.name}' detected", 15)

    if check_notify_method(node.name):
        _analyze_notification_method(node, add_evidence_func)


def _analyze_notification_method(node: ast.FunctionDef, add_evidence_func) -> None:
    """Analyze a potential notification method."""
    add_evidence_func(f"Notification method '{node.name}' detected", 15)
    if check_iteration(node):
        add_evidence_func("Notification method iterates over collection", 30)
