from typing import Dict, Any, List, Set, Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def count_edges(import_graph: Dict[str, Set[str]]) -> int:
    """Counts total edges in the dependency graph.

    Args:
        import_graph: A dictionary where keys are module paths and values are sets of imported module paths.

    Returns:
        The total number of edges (imports) in the graph.
    """
    return sum(len(neighbors) for neighbors in import_graph.values())


def find_simple_cycles(import_graph: Dict[str, Set[str]], limit: int = 5) -> List[List[str]]:
    """Detects simple cycles in the import graph using Depth First Search.

    Args:
        import_graph: A graph representing internal project imports.
        limit: Maximum number of cycles to detect before stopping. Defaults to 5.

    Returns:
        A list of cycles, where each cycle is a list of module paths.
    """
    cycles = []
    visited = set()
    path = []
    path_set = set()

    def dfs(u):
        if len(cycles) >= limit:
            return

        visited.add(u)
        path.append(u)
        path_set.add(u)

        if u in import_graph:
            for v in import_graph[u]:
                if v in path_set:
                    # Cycle detected
                    cycle_start = path.index(v)
                    cycles.append(path[cycle_start:])
                elif v not in visited:
                    dfs(v)

        path_set.remove(u)
        path.pop()

    for node in list(import_graph.keys()):
        if node not in visited:
            dfs(node)

    return cycles


def count_connected_components(import_graph: Dict[str, Set[str]]) -> int:
    """Counts weakly connected components in the dependency graph.

    Args:
        import_graph: The project's import graph.

    Returns:
        The number of weakly connected components.
    """
    # Convert to undirected graph
    undirected = {}
    for u, neighbors in import_graph.items():
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
            # BFS traversal
            queue = [node]
            visited.add(node)
            while queue:
                curr = queue.pop(0)
                for neighbor in undirected.get(curr, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return count


def calculate_coupling_metrics(
    import_graph: Dict[str, Set[str]],
) -> Dict[str, Dict[str, int]]:
    """Calculates Coupling Between Objects (CBO) metrics for each module.

    Args:
        import_graph: The project's internal import graph.

    Returns:
        A dictionary mapping module paths to their coupling scores (fan-in and fan-out).
    """
    metrics = {}
    all_nodes = set(import_graph.keys())
    for neighbors in import_graph.values():
        all_nodes.update(neighbors)

    fan_in = {node: 0 for node in all_nodes}
    fan_out = {node: 0 for node in all_nodes}

    for u, neighbors in import_graph.items():
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
    """Analyzes project dependencies, builds the import graph, and detects circularities.

    Args:
        modules_data: List of dictionaries containing module analysis results.
        project_path: Root directory of the project.
        read_file_func: Utility function to read file contents.

    Returns:
        A dictionary containing categorized imports, graph metrics, and identified cycles.
    """
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

    # 2. Build import graph
    import_graph = _build_import_graph(modules_data)
    dependencies["import_graph"] = {k: list(v) for k, v in import_graph.items()}

    # 3. Detect circular dependencies
    try:
        cycles = find_simple_cycles(import_graph, limit=5)
        if cycles:
            dependencies["circular_dependencies"] = cycles
    except Exception:
        pass

    # 4. Calculate graph metrics and coupling
    dependencies["graph_metrics"] = _calculate_graph_metrics(import_graph)
    dependencies["coupling_metrics"] = calculate_coupling_metrics(import_graph)

    # 5. Collect unused imports from modules_data
    unused_imports = {}
    for mod in modules_data:
        if mod.get("unused_imports"):
            unused_imports[mod["path"]] = mod["unused_imports"]
    dependencies["unused_imports"] = unused_imports

    # 6. Classify imports
    all_imports = set()
    for module in modules_data:
        all_imports.update(module.get("imports", []))

    classified = _classify_imports(all_imports)
    dependencies.update(classified)

    return dependencies


def _parse_dependency_files(project_path: Path, read_file_func: Callable) -> Dict[str, str]:
    """Reads content from common dependency files (e.g., requirements.txt, pyproject.toml).

    Args:
        project_path: Root directory to search in.
        read_file_func: Function used to read file contents.

    Returns:
        A dictionary mapping filenames to their filtered contents.
    """
    files_content = {}
    req_files = [
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "Pipfile",
        "setup.cfg",
        "environment.yml",
    ]

    for req_file in req_files:
        path = project_path / req_file
        if path.exists():
            try:
                content = read_file_func(path)
                if content:
                    files_content[req_file] = content[
                        :2000
                    ]  # Limit size for documentation purposes
            except Exception:
                pass
    return files_content


def _build_import_graph(modules_data: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """Builds a directed graph representing internal imports between project modules.

    Args:
        modules_data: Raw analysis data from all project modules.

    Returns:
        A dictionary mapping source module paths to sets of target module paths.
    """
    import_graph = {}
    # Create valid target module names (dots instead of slashes)
    module_names = {}
    for mod in modules_data:
        path = mod.get("path", "")
        if path:
            # Map "pkg/sub/mod.py" -> "pkg.sub.mod"
            canonical = path.replace(".py", "").replace("/", ".").replace("\\", ".")
            module_names[canonical] = path

    for module in modules_data:
        module_path = module.get("path", "")
        imports = module.get("imports", [])

        if module_path:
            if module_path not in import_graph:
                import_graph[module_path] = set()

            for imp in imports:
                # Check if import refers to an internal project module
                for canonical, target_path in module_names.items():
                    if canonical in imp:
                        import_graph[module_path].add(target_path)
                        if target_path not in import_graph:
                            import_graph[target_path] = set()
                        break
    return import_graph


def _calculate_graph_metrics(import_graph: Dict[str, Set[str]]) -> Dict[str, Any]:
    """Calculates density, connectivity, and acyclicity metrics for the import graph.

    Args:
        import_graph: The project's import graph.

    Returns:
        A dictionary with node/edge counts, density, and graph properties.
    """
    num_nodes = len(import_graph)
    if num_nodes == 0:
        return {}

    try:
        num_edges = count_edges(import_graph)
        # Density for directed graph: E / (V * (V - 1))
        max_edges = num_nodes * (num_nodes - 1)
        density = num_edges / max_edges if max_edges > 0 else 0

        return {
            "nodes": num_nodes,
            "edges": num_edges,
            "density": density,
            "is_dag": len(find_simple_cycles(import_graph, limit=1)) == 0,
            "weakly_connected_components": count_connected_components(import_graph),
        }
    except Exception as e:
        logger.exception(f"Error calculating graph metrics: {e}")
        return {}


def _classify_imports(all_imports: Set[str]) -> Dict[str, List[str]]:
    """Categorizes imports into internal, external (StdLib), and third-party modules.

    Args:
        all_imports: A combined set of all import strings found in the project.

    Returns:
        A dictionary with three lists: internal, external, and third_party.
    """
    stdlib_modules = {
        "os",
        "sys",
        "json",
        "pathlib",
        "typing",
        "datetime",
        "re",
        "collections",
        "itertools",
        "math",
        "random",
        "statistics",
        "functools",
        "hashlib",
        "base64",
        "csv",
        "pickle",
        "sqlite3",
        "subprocess",
        "logging",
        "time",
        "traceback",
        "ast",
        "abc",
        "threading",
        "multiprocessing",
        "concurrent",
        "shutil",
        "tempfile",
    }

    results = {"internal": [], "external": [], "third_party": []}

    for imp in sorted(all_imports):
        # Determine if it's internal (relative or project-specific)
        if imp.startswith(".") or any(seg in imp for seg in ["..", "./"]):
            results["internal"].append(imp)
        # Determine if it's part of the Python Standard Library
        elif imp.split(".")[0] in stdlib_modules:
            results["external"].append(imp)
        else:
            results["third_party"].append(imp)

    return results
