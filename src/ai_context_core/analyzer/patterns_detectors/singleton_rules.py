"""Compatibility facade for singleton rules."""

from ..visitors.singleton_rules import (
    _is_singleton_instance_var,
    _check_singleton_new,
    _check_singleton_get_instance,
    check_singleton_method,
)

__all__ = [
    "_is_singleton_instance_var",
    "_check_singleton_new",
    "_check_singleton_get_instance",
    "check_singleton_method",
]
