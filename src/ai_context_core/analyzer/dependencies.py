from .builders.dependencies import *  # noqa: F403
from .builders.algorithms import CycleDetector, GraphMetricsCalculator
from .builders.classifier import classify_imports as _classify_imports  # noqa: F401
from .builders.parser import parse_dependency_files as _parse_dependency_files  # noqa: F401


def find_simple_cycles(graph, limit=5):
    return CycleDetector(graph, limit=limit).find_cycles()


def calculate_coupling_metrics(graph):
    return GraphMetricsCalculator(graph).calculate_coupling_metrics()


def count_edges(graph):
    return GraphMetricsCalculator(graph).count_edges()


def count_connected_components(graph):
    return GraphMetricsCalculator(graph).count_connected_components()
