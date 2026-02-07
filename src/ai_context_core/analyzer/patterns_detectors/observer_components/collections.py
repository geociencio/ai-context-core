"""Observer collection management rules."""

import ast

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
    """Checks if assignment is for an observer collection."""
    for t in node.targets:
        if isinstance(t, ast.Attribute) and any(
            kw in t.attr.lower() for kw in KEYWORDS_INIT
        ):
            return True
    return False


def check_iteration(node: ast.AST) -> bool:
    """Checks for iteration over observer collections."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.For):
            iter_str = ast.unparse(sub.iter).lower()
            if any(kw in iter_str for kw in KEYWORDS_INIT):
                return True
    return False


def check_mgmt_method(name: str) -> bool:
    """Checks if method name matches management patterns."""
    m_low = name.lower()
    return any(kw in m_low for kw in KEYWORDS_MGMT)


def check_notify_method(name: str) -> bool:
    """Checks if method name matches notification patterns."""
    m_low = name.lower()
    return any(kw in m_low for kw in KEYWORDS_NOTIFY)
