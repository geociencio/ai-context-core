from .builders.dependencies import *  # noqa: F403
from .builders.algorithms import CycleDetector, GraphMetricsCalculator


def find_simple_cycles(graph, limit=5):
    return CycleDetector(graph, limit=limit).find_cycles()


def calculate_coupling_metrics(graph):
    return GraphMetricsCalculator(graph).calculate_coupling_metrics()


def count_edges(graph):
    return GraphMetricsCalculator(graph).count_edges()


def count_connected_components(graph):
    return GraphMetricsCalculator(graph).count_connected_components()
