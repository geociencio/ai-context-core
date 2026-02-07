"""Graph coupling metrics (Fan-In, Fan-Out, CBO)."""

from typing import Dict, Set


def calculate_coupling(graph: Dict[str, Set[str]]) -> Dict[str, Dict[str, int]]:
    """Calculate Fan-In, Fan-Out, and CBO for each node.

    Args:
        graph: Project dependency graph.

    Returns:
        Dictionary mapping node paths to their coupling metrics.
    """
    all_nodes = _get_all_nodes(graph)
    fan_in = {node: 0 for node in all_nodes}
    fan_out = {node: 0 for node in all_nodes}

    for u, neighbors in graph.items():
        fan_out[u] = len(neighbors)
        for v in neighbors:
            fan_in[v] += 1

    return {
        node: {
            "fan_in": fan_in[node],
            "fan_out": fan_out[node],
            "cbo": fan_in[node] + fan_out[node],
        }
        for node in all_nodes
    }


def _get_all_nodes(graph: Dict[str, Set[str]]) -> Set[str]:
    """Retrieves all unique node names in the graph."""
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)
    return nodes
