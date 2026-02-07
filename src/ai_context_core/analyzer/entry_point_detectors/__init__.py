"""Entry point detectors package."""

from .base import BaseEntryPointRule
from .framework_rules import DecoratorRule, AssignmentRule

__all__ = ["BaseEntryPointRule", "DecoratorRule", "AssignmentRule"]
