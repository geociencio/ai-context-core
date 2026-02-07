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
