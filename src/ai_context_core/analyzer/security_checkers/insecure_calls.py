"""Compatibility facade for insecure calls checker."""

from ..visitors.insecure_calls import InsecureCallsChecker
from ..visitors.ast_security import detect_ast_security_issues

__all__ = ["InsecureCallsChecker", "detect_ast_security_issues"]
