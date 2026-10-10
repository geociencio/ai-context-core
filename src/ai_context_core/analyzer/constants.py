"""Constants for the analyzer module to avoid magic numbers.

Only constants still consumed by the context-only codebase live here; the
analysis-domain thresholds were removed in v5.0.0.
"""

# Complexity penalty tuning (ComplexityVisitor)
COMPLEXITY_PENALTY_DENSITY_THRESHOLD = 0.5
COMPLEXITY_PENALTY_MULTIPLIER = 1.2

# Parallel processing (worker.py)
PARALLEL_MIN_FILES = 5
PARALLEL_BATCH_SIZE = 10
