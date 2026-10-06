"""Core helpers for the golden fixture plugin."""

MODE = "golden"


def compute(value):
    """Double a non-negative value, clamping negatives to zero."""
    if value < 0:
        return 0
    return value * 2
