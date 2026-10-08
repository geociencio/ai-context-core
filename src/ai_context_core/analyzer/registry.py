"""Centralized registry for analysis components (detectors)."""

import logging
from typing import Dict, Callable

logger = logging.getLogger(__name__)


class AnalysisRegistry:
    """Registry for managing analysis extensions."""

    def __init__(self):
        self._detectors: Dict[str, Callable] = {}

    def register_detector(self, name: str, detector_func: Callable):
        """Registers a detection function."""
        self._detectors[name] = detector_func
        logger.debug(f"Registered detector: {name}")

    @property
    def detectors(self) -> Dict[str, Callable]:
        """Return registered detectors."""
        return self._detectors


# Global instance
registry = AnalysisRegistry()


def register_detector(name: str):
    """Decorator for registering detectors."""

    def wrapper(func):
        registry.register_detector(name, func)
        return func

    return wrapper
