"""Graph connectivity analysis (components)."""

from typing import Dict, Set

def count_connected_components(graph: Dict[str, Set[str]]) -> int:
    """Count weakly connected components in the graph.

    Args:
        graph: Directed adjacency list.

    Returns:
        Number of weakly connected components.
    """
    undirected = _build_undirected(graph)
    visited = set()
    count = 0
    for node in undirected:
        if node not in visited:
            count += 1
            _bfs_visit(node, visited, undirected)
    return count

def _build_undirected(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Convers a directed graph into an undirected adjacency list."""
    undirected = {}
    for u, neighbors in graph.items():
        if u not in undirected:
            undirected[u] = set()
        for v in neighbors:
            undirected[u].add(v)
            if v not in undirected:
                undirected[v] = set()
            undirected[v].add(u)
    return undirected

def _bfs_visit(start_node: str, visited: Set[str], undirected: Dict[str, Set[str]]):
    """BFS traversal for component counting."""
    queue = [start_node]
    visited.add(start_node)
    while queue:
        curr = queue.pop(0)
        for neighbor in undirected.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
