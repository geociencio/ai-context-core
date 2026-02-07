"""Calculation of dependency graph metrics."""

from typing import Dict, List, Set

class GraphMetricsCalculator:
    """Class to calculate various graph metrics."""

    def __init__(self, import_graph: Dict[str, Set[str]]):
        """Initialize the graph metrics calculator.

        Args:
            import_graph: Project dependency graph.
        """
        self.graph = import_graph
        self.num_nodes = len(import_graph)

from .metrics_components import count_connected_components as _count_comp, calculate_coupling as _calc_coupling

class GraphMetricsCalculator:
    """Class to calculate various graph metrics.
    
    Delegates complex algorithms to specialized components.
    """

    def __init__(self, import_graph: Dict[str, Set[str]]):
        """Initialize the graph metrics calculator.

        Args:
            import_graph: Project dependency graph.
        """
        self.graph = import_graph
        self.num_nodes = len(import_graph)

    def count_edges(self) -> int:
        """Count total edges in the graph.

        Returns:
            Total count of directed edges.
        """
        return sum(len(neighbors) for neighbors in self.graph.values())

    def calculate_density(self, num_edges: int) -> float:
        """Calculate graph density.

        Args:
            num_edges: Total number of edges in the graph.

        Returns:
            Density value (edges / max_possible_edges).
        """
        max_edges = self.num_nodes * (self.num_nodes - 1)
        return num_edges / max_edges if max_edges > 0 else 0

    def count_connected_components(self) -> int:
        """Count weakly connected components in the graph.

        Returns:
            Number of weakly connected components.
        """
        return _count_comp(self.graph)

    def calculate_coupling_metrics(self) -> Dict[str, Dict[str, int]]:
        """Calculate Fan-In, Fan-Out, and CBO for each node.

        Returns:
            Dictionary mapping node paths to their coupling metrics.
        """
        return _calc_coupling(self.graph)
