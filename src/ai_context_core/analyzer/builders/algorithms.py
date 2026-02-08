"""Graph algorithms for dependency analysis."""

from typing import Dict, List, Set


class CycleDetector:
    """Class responsible for detecting cycles in the graph."""

    def __init__(self, graph: Dict[str, Set[str]], limit: int = 5):
        """Initialize the cycle detector.

        Args:
            graph: Dependency graph (adj. list of module paths).
            limit: Maximum number of cycles to detect.
        """
        self.graph = graph
        self.limit = limit
        self.cycles = []
        self.visited = set()
        self.path = []
        self.path_set = set()

    def find_cycles(self) -> List[List[str]]:
        """Find simple cycles in the graph up to the configured limit.

        Returns:
            List of detected cycles, each cycle is a list of node paths.
        """
        for node in list(self.graph.keys()):
            if node not in self.visited:
                self._dfs(node)
        return self.cycles

    def _dfs(self, u: str):
        """Perform recursive DFS to detect cycles.

        Args:
            u: Current node path.
        """
        if len(self.cycles) >= self.limit:
            return

        self.visited.add(u)
        self.path.append(u)
        self.path_set.add(u)

        if u in self.graph:
            for v in self.graph[u]:
                if v in self.path_set:
                    cycle_start = self.path.index(v)
                    self.cycles.append(self.path[cycle_start:])
                elif v not in self.visited:
                    self._dfs(v)

        self.path_set.remove(u)
        self.path.pop()


class GraphMetricsCalculator:
    """Class to calculate various graph metrics."""

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
        undirected = self._build_undirected()
        visited = set()
        count = 0
        for node in undirected:
            if node not in visited:
                count += 1
                self._bfs_visit(node, visited, undirected)
        return count

    def _build_undirected(self) -> Dict[str, Set[str]]:
        """Converts a directed graph into an undirected adjacency list."""
        undirected = {}
        for u, neighbors in self.graph.items():
            if u not in undirected:
                undirected[u] = set()
            for v in neighbors:
                undirected[u].add(v)
                if v not in undirected:
                    undirected[v] = set()
                undirected[v].add(u)
        return undirected

    def _bfs_visit(
        self, start_node: str, visited: Set[str], undirected: Dict[str, Set[str]]
    ):
        """BFS traversal for component counting."""
        queue = [start_node]
        visited.add(start_node)
        while queue:
            curr = queue.pop(0)
            for neighbor in undirected.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def calculate_coupling_metrics(self) -> Dict[str, Dict[str, int]]:
        """Calculate Fan-In, Fan-Out, and CBO for each node.

        Returns:
            Dictionary mapping node paths to their coupling metrics.
        """
        all_nodes = self._get_all_nodes()
        fan_in = {node: 0 for node in all_nodes}
        fan_out = {node: 0 for node in all_nodes}

        for u, neighbors in self.graph.items():
            if u in fan_out:
                fan_out[u] = len(neighbors)
            for v in neighbors:
                if v in fan_in:
                    fan_in[v] += 1

        return {
            node: {
                "fan_in": fan_in[node],
                "fan_out": fan_out[node],
                "cbo": fan_in[node] + fan_out[node],
            }
            for node in all_nodes
        }

    def _get_all_nodes(self) -> Set[str]:
        """Retrieves all unique node names in the graph."""
        nodes = set(self.graph.keys())
        for neighbors in self.graph.values():
            nodes.update(neighbors)
        return nodes
