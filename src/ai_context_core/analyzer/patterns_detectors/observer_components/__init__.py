"""Observer components package."""

from .signals import detect_signals
from .collections import (
    check_init_assign, check_iteration, check_mgmt_method, 
    check_notify_method, KEYWORDS_INIT, KEYWORDS_MGMT, KEYWORDS_NOTIFY
)
from .class_analyzer import analyze_class_body

__all__ = [
    "detect_signals", "check_init_assign", "check_iteration", 
    "check_mgmt_method", "check_notify_method", "analyze_class_body"
]
