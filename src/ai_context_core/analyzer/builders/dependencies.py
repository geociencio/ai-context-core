"""Dependency analysis and builders for ai-context-core."""

from typing import Dict, Any, List, Callable
import sys
import logging
import pathlib
from .algorithms import CycleDetector, GraphMetricsCalculator
from .context_base import BaseContextBuilder

logger = logging.getLogger(__name__)

# Get standard library modules dynamically (Python 3.10+)
if sys.version_info >= (3, 10):
    STDLIB_MODULES = sys.stdlib_module_names
else:
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


def analyze_dependencies(
    modules_data: List[Dict[str, Any]],
    project_path: pathlib.Path,
    read_file_func: Callable,
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
    from .parser import parse_dependency_files

    dependencies["files"] = parse_dependency_files(project_path, read_file_func)

    # 2. Build import graph and identify internal modules
    from .builder import ImportGraphBuilder

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

    from .classifier import classify_imports

    classified = classify_imports(all_imports, STDLIB_MODULES, known_internal)
    dependencies.update(classified)

    return dependencies


class DependencyAnalyzer:
    """Legacy wrapper for dependency analysis."""

    def __init__(self, project_path: pathlib.Path):
        """Initialize the legacy analyzer."""
        self.project_path = project_path

    def build_graph(self, modules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build the dependency graph for the project."""

        def _read_file(p: pathlib.Path) -> str:
            return p.read_text(errors="ignore")

        return analyze_dependencies(modules_data, self.project_path, _read_file)


def detect_unused_imports_in_project(
    modules_data: List[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """Collects unused imports across all modules."""
    unused = {}
    for mod in modules_data:
        if mod.get("unused_imports"):
            unused[mod["path"]] = mod["unused_imports"]
    return unused


class DependencyBuilder(BaseContextBuilder):
    """Adds dependency analysis and optimizations for AI context."""

    def build(self, lines: List[str]) -> None:
        from .reporting import generate_dependency_diagram

        deps = self.analyses.get("dependencies", {})
        lines.append("\n## 🔗 PRIMARY DEPENDENCIES")
        tp = deps.get("third_party", [])
        if tp:
            counts = {}
            for d in tp:
                base = d.split(".")[0]
                counts[base] = counts.get(base, 0) + 1
            lines.append("### Third Party (most frequent):")
            for p, c in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:15]:
                lines.append(f"- `{p}` ({c} imports)")

        unused = deps.get("unused_imports", {})
        if unused:
            lines.append("\n## ⚠️ UNUSED IMPORTS")
            for mod, items in list(unused.items())[:5]:
                lines.append(f"- **{mod}**: {', '.join(items[:5])}")

        high_c = sorted(
            deps.get("coupling_metrics", {}).items(),
            key=lambda x: x[1].get("cbo", 0),
            reverse=True,
        )[:5]
        high_c = [i for i in high_c if i[1].get("cbo", 0) > 5]
        if high_c:
            lines.append("\n## 🔗 HIGH COUPLING MODULES (CBO)")
            for mod, m_val in high_c:
                lines.append(
                    f"- **{mod}**: CBO {m_val['cbo']} (In: {m_val['fan_in']}, Out: {m_val['fan_out']})"
                )

        g_m = deps.get("graph_metrics", {})
        if g_m:
            lines.append("\n## 🕸️  DEPENDENCY STRUCTURE")
            lines.append(
                f"- **Nodes**: {g_m.get('nodes', 0)}\n- **Edges**: {g_m.get('edges', 0)}\n- **Density**: {g_m.get('density', 0):.3f}"
            )
            lines.append("\n## 🕸️ DEPENDENCY DIAGRAM (Conceptual)\n```mermaid")
            lines.append(generate_dependency_diagram(deps))
            lines.append("```")

        # Optimizations
        opts = self.analyses.get("optimizations", [])
        if opts:
            lines.append("\n## 💡 OPTIMIZATION RECOMMENDATIONS")
            for o in opts[:5]:
                lines.append(f"### {o.get('module')}")
                for sug in o.get("suggestions", [])[:2]:
                    lines.append(
                        f"- **{sug.get('type', 'Opt')}**: {sug.get('message', 'N/A')}"
                    )


def find_simple_cycles(graph, limit=5):
    from .algorithms import CycleDetector

    detector = CycleDetector(graph, limit=limit)
    return detector.find_cycles()


def count_edges(graph):
    from .algorithms import GraphMetricsCalculator

    return GraphMetricsCalculator(graph).count_edges()


def count_connected_components(graph):
    from .algorithms import GraphMetricsCalculator

    return GraphMetricsCalculator(graph).count_connected_components()


def calculate_coupling_metrics(graph):
    from .algorithms import GraphMetricsCalculator

    return GraphMetricsCalculator(graph).calculate_coupling_metrics()


def calculate_density(graph, edges):
    from .algorithms import GraphMetricsCalculator

    calc = GraphMetricsCalculator(graph)
    # GraphMetricsCalculator.calculate_density takes 1 arg (num_edges)
    # but uses self.num_nodes.
    return calc.calculate_density(edges)


# Legacy internal aliases
def _classify_imports(*args, **kwargs):
    from .classifier import classify_imports

    return classify_imports(*args, **kwargs)


def _parse_dependency_files(*args, **kwargs):
    from .parser import parse_dependency_files

    return parse_dependency_files(*args, **kwargs)


STDLIB_MODULES = STDLIB_MODULES  # expose it
