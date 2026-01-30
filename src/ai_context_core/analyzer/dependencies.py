"""Dependency analysis module for Python projects."""

from typing import Dict, Any, List, Set, Callable, Optional
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# Get standard library modules dynamically (Python 3.10+)
# Fallback for older python versions if needed, though project requires >=3.9
if sys.version_info >= (3, 10):
    STDLIB_MODULES = sys.stdlib_module_names
else:
    # Minimal fallback or rely on isort/stdlib-list if installed,
    # but for zero-deps we keep a larger hardcoded list or just accept imperfection on <3.10
    # Extending the previous list slightly for better coverage on 3.9
    STDLIB_MODULES = {
        "abc",
        "argparse",
        "ast",
        "asyncio",
        "base64",
        "collections",
        "concurrent",
        "contextlib",
        "copy",
        "csv",
        "datetime",
        "decimal",
        "email",
        "enum",
        "functools",
        "hashlib",
        "html",
        "http",
        "importlib",
        "inspect",
        "io",
        "itertools",
        "json",
        "logging",
        "math",
        "multiprocessing",
        "os",
        "pathlib",
        "pickle",
        "platform",
        "random",
        "re",
        "shutil",
        "socket",
        "sqlite3",
        "statistics",
        "subprocess",
        "sys",
        "tempfile",
        "threading",
        "time",
        "traceback",
        "typing",
        "unittest",
        "urllib",
        "uuid",
        "warnings",
        "xml",
        "zipfile",
    }

DEPENDENCY_FILES = [
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
    "Pipfile",
    "setup.cfg",
    "environment.yml",
]


class ImportGraphBuilder:
    """Class responsible for building the internal import graph of the project."""

    def __init__(self, modules_data: List[Dict[str, Any]]):
        """Initialize the builder with module data."""
        self.modules_data = modules_data
        self.import_graph = {}
        self.import_map = {}
        self.known_internal_modules = set()

    def build(self) -> Dict[str, Set[str]]:
        """Build and return the import graph."""
        self._initialize_graph()
        self._resolve_imports()
        return self.import_graph

    def _initialize_graph(self):
        """Initialize graph nodes and populate import map."""
        for mod in self.modules_data:
            path = mod.get("path", "")
            if not path:
                continue

            if path not in self.import_graph:
                self.import_graph[path] = set()

            importable = self._add_to_import_map(path)
            if importable:
                self.known_internal_modules.add(importable)

    def _add_to_import_map(self, path: str) -> Optional[str]:
        """Map importable python paths to file paths.

        Args:
            path: Relative file path of the module.

        Returns:
            The importable python path (e.g., 'pkg.mod') if successful.

        """
        clean_path = path.replace("\\", "/")
        # Heuristic: assume 'src/' matches package root if present
        if clean_path.startswith("src/"):
            clean_path = clean_path[4:]

        # Also handle common 'lib/' or just root based paths
        # This is a simplification; ideally we'd look for __init__.py recursively

        importable = clean_path.replace(".py", "").replace("/", ".")
        if importable.endswith(".__init__"):
            importable = importable[:-9]

        self.import_map[importable] = path
        return importable

    def _resolve_imports(self):
        """Iterate through modules and resolve their imports to project files."""
        for module in self.modules_data:
            source_path = module.get("path", "")
            if not source_path:
                continue

            for imp in module.get("imports", []):
                target = self._resolve_single_import(imp)
                if target and target != source_path:
                    self.import_graph[source_path].add(target)

    def _resolve_single_import(self, imp: str) -> Optional[str]:
        """Resolve a single import string to a file path.

        Args:
            imp: Import string (e.g., 'pkg.mod').

        Returns:
            Resolved file path or None if not found in project.

        """
        # Direct match
        if imp in self.import_map:
            return self.import_map[imp]

        # Parent match (imp='pkg.mod.Class') -> matches 'pkg.mod'
        if "." in imp:
            parts = imp.split(".")
            # Try progressively shorter prefixes
            for i in range(len(parts), 0, -1):
                prefix = ".".join(parts[:i])
                if prefix in self.import_map:
                    return self.import_map[prefix]

        return None


class CycleDetector:
    """Class responsible for detecting cycles in the graph."""

    def __init__(self, graph: Dict[str, Set[str]], limit: int = 5):
        """Initialize the detector."""
        self.graph = graph
        self.limit = limit
        self.cycles = []
        self.visited = set()
        self.path = []
        self.path_set = set()

    def find_cycles(self) -> List[List[str]]:
        """Find simple cycles in the graph up to the configured limit."""
        for node in list(self.graph.keys()):
            if node not in self.visited:
                self._dfs(node)
        return self.cycles

    def _dfs(self, u: str):
        """Perform recursive DFS to detect cycles."""
        if len(self.cycles) >= self.limit:
            return

        self.visited.add(u)
        self.path.append(u)
        self.path_set.add(u)

        if u in self.graph:
            for v in self.graph[u]:
                if v in self.path_set:
                    # Cycle detected
                    cycle_start = self.path.index(v)
                    self.cycles.append(self.path[cycle_start:])
                elif v not in self.visited:
                    self._dfs(v)

        self.path_set.remove(u)
        self.path.pop()


class GraphMetricsCalculator:
    """Class to calculate various graph metrics."""

    def __init__(self, import_graph: Dict[str, Set[str]]):
        """Initialize with an import graph."""
        self.graph = import_graph
        self.num_nodes = len(import_graph)

    def count_edges(self) -> int:
        """Count total edges in the graph."""
        return sum(len(neighbors) for neighbors in self.graph.values())

    def calculate_density(self, num_edges: int) -> float:
        """Calculate graph density."""
        max_edges = self.num_nodes * (self.num_nodes - 1)
        return num_edges / max_edges if max_edges > 0 else 0

    def count_connected_components(self) -> int:
        """Count weakly connected components in the graph."""
        # Convert to undirected graph
        undirected = {}
        for u, neighbors in self.graph.items():
            if u not in undirected:
                undirected[u] = set()
            for v in neighbors:
                undirected[u].add(v)
                if v not in undirected:
                    undirected[v] = set()
                undirected[v].add(u)

        visited = set()
        count = 0
        for node in undirected:
            if node not in visited:
                count += 1
                self._bfs_visit(node, visited, undirected)
        return count

    def _bfs_visit(
        self, start_node: str, visited: Set[str], undirected: Dict[str, Set[str]]
    ):
        """Perform BFS traversal for component counting."""
        queue = [start_node]
        visited.add(start_node)
        while queue:
            curr = queue.pop(0)
            for neighbor in undirected.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def calculate_coupling_metrics(self) -> Dict[str, Dict[str, int]]:
        """Calculate Fan-In, Fan-Out, and CBO for each node."""
        metrics = {}
        all_nodes = set(self.graph.keys())
        for neighbors in self.graph.values():
            all_nodes.update(neighbors)

        fan_in = {node: 0 for node in all_nodes}
        fan_out = {node: 0 for node in all_nodes}

        for u, neighbors in self.graph.items():
            fan_out[u] = len(neighbors)
            for v in neighbors:
                fan_in[v] += 1

        for node in all_nodes:
            metrics[node] = {
                "fan_in": fan_in[node],
                "fan_out": fan_out[node],
                "cbo": fan_in[node] + fan_out[node],
            }
        return metrics


def analyze_dependencies(
    modules_data: List[Dict[str, Any]], project_path: Path, read_file_func: Callable
) -> Dict[str, Any]:
    """Analyzes project dependencies, builds the import graph, and detects circularities."""
    dependencies = {
        "internal": [],
        "external": [],
        "third_party": [],
        "files": {},
        "import_graph": {},
        "circular_dependencies": [],
        "graph_metrics": {},
    }

    # 1. Parse common dependency files
    dependencies["files"] = _parse_dependency_files(project_path, read_file_func)

    # 2. Build import graph and identify internal modules
    builder = ImportGraphBuilder(modules_data)
    import_graph = builder.build()
    dependencies["import_graph"] = {k: list(v) for k, v in import_graph.items()}

    # Store known internal module names for classification
    known_internal = builder.known_internal_modules

    # 3. Detect circular dependencies
    try:
        detector = CycleDetector(import_graph, limit=5)
        cycles = detector.find_cycles()
        if cycles:
            dependencies["circular_dependencies"] = cycles
    except Exception:
        pass

    # 4. Calculate graph metrics
    metrics_calc = GraphMetricsCalculator(import_graph)
    try:
        num_edges = metrics_calc.count_edges()
        dependencies["graph_metrics"] = {
            "nodes": len(import_graph),
            "edges": num_edges,
            "density": metrics_calc.calculate_density(num_edges),
            "is_dag": len(CycleDetector(import_graph, limit=1).find_cycles()) == 0,
            "weakly_connected_components": metrics_calc.count_connected_components(),
        }
        dependencies["coupling_metrics"] = metrics_calc.calculate_coupling_metrics()
    except Exception as e:
        logger.exception(f"Error calculating graph metrics: {e}")

    # 5. Collect unused imports
    unused_imports = {}
    for mod in modules_data:
        if mod.get("unused_imports"):
            unused_imports[mod["path"]] = mod["unused_imports"]
    dependencies["unused_imports"] = unused_imports

    # 6. Classify imports
    all_imports = set()
    for module in modules_data:
        all_imports.update(module.get("imports", []))

    classified = _classify_imports(all_imports, known_internal)
    dependencies.update(classified)

    return dependencies


def _parse_dependency_files(
    project_path: Path, read_file_func: Callable
) -> Dict[str, str]:
    """Read content from common dependency files."""
    files_content = {}
    for req_file in DEPENDENCY_FILES:
        path = project_path / req_file
        if path.exists():
            try:
                content = read_file_func(path)
                if content:
                    files_content[req_file] = content[:2000]
            except Exception:
                pass
    return files_content


def _classify_imports(
    all_imports: Set[str], known_internal: Set[str] = None
) -> Dict[str, List[str]]:
    """Categorizes imports into internal, external (StdLib), and third-party modules.

    Args:
        all_imports: Set of all import strings found in the project.
        known_internal: Set of known internal module names (optional).

    """
    results = {"internal": [], "external": [], "third_party": []}
    known_internal = known_internal or set()

    for imp in sorted(all_imports):
        root_pkg = imp.split(".")[0]

        # Check for explicitly known internal modules
        is_known_internal = False
        if imp in known_internal:
            is_known_internal = True
        else:
            # Check prefixes (e.g., if 'my_pkg.utils' is known, 'my_pkg' should be internal too?)
            # Actually, reverse: if 'my_pkg' is in known_internal, 'my_pkg.utils' is internal.
            # But known_internal usually contains full paths 'my_pkg.utils'.
            # We need to check if 'imp' or any parent is in known_internal.
            # A simpler heuristic for this step: check if root package matches any known internal root
            for internal in known_internal:
                if imp == internal or imp.startswith(internal + "."):
                    is_known_internal = True
                    break

        if (
            is_known_internal
            or imp.startswith(".")
            or any(seg in imp for seg in ["..", "./"])
        ):
            results["internal"].append(imp)
        elif root_pkg in STDLIB_MODULES:
            results["external"].append(imp)
        else:
            results["third_party"].append(imp)

    return results


# Re-export legacy functions if needed for API compatibility,
# although they are now mostly handled by classes internally.
# Exposing them as simple wrappers just in case.


def count_edges(import_graph: Dict[str, Set[str]]) -> int:
    """Count total edges in the graph (Legacy wrapper)."""
    return GraphMetricsCalculator(import_graph).count_edges()


def find_simple_cycles(
    import_graph: Dict[str, Set[str]], limit: int = 5
) -> List[List[str]]:
    """Find simple cycles in the graph (Legacy wrapper)."""
    return CycleDetector(import_graph, limit).find_cycles()


def count_connected_components(import_graph: Dict[str, Set[str]]) -> int:
    """Count connected components (Legacy wrapper)."""
    return GraphMetricsCalculator(import_graph).count_connected_components()


def calculate_coupling_metrics(
    import_graph: Dict[str, Set[str]],
) -> Dict[str, Dict[str, int]]:
    """Calculate coupling metrics (Legacy wrapper)."""
    return GraphMetricsCalculator(import_graph).calculate_coupling_metrics()
