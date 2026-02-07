"""Centralized registry for analysis components (visitors, detectors, processors).

Allows for dynamic discovery and simplified orchestration of analysis rules.
"""

import logging
from typing import Dict, Any, List, Callable, Type

logger = logging.getLogger(__name__)


class AnalysisRegistry:
    """Registry for managing analysis extensions."""

    def __init__(self):
        self._visitors: List[Type] = []
        self._detectors: Dict[str, Callable] = {}
        self._post_processors: List[Callable] = []

    def register_visitor(self, visitor_class: Type):
        """Registers an AST visitor class."""
        self._visitors.append(visitor_class)
        logger.debug(f"Registered visitor: {visitor_class.__name__}")

    def register_detector(self, name: str, detector_func: Callable):
        """Registers a detection function."""
        self._detectors[name] = detector_func
        logger.debug(f"Registered detector: {name}")

    def register_post_processor(self, processor_func: Callable):
        """Registers a post-analysis processing function."""
        self._post_processors.append(processor_func)
        logger.debug(f"Registered post-processor: {processor_func.__name__}")

    @property
    def visitors(self) -> List[Type]:
        """Return registered visitors."""
        return self._visitors

    @property
    def detectors(self) -> Dict[str, Callable]:
        """Return registered detectors."""
        return self._detectors

    @property
    def post_processors(self) -> List[Callable]:
        """Return registered post-processors."""
        return self._post_processors


# Global instance
registry = AnalysisRegistry()


def register_visitor(cls):
    """Decorator for registering visitors."""
    registry.register_visitor(cls)
    return cls


def register_detector(name: str):
    """Decorator for registering detectors."""
    def wrapper(func):
        registry.register_detector(name, func)
        return func
    return wrapper
