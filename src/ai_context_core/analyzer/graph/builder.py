"""Logic for building the project import graph."""

from typing import Dict, Any, List, Set
from .builder_components import get_importable_path, resolve_import

class ImportGraphBuilder:
    """Class responsible for building the internal import graph of the project.
    
    Delegates path mapping and resolution to specialized components.
    """

    def __init__(self, modules_data: List[Dict[str, Any]]):
        """Initialize the builder with module data.

        Args:
            modules_data: List of module analysis results.
        """
        self.modules_data = modules_data
        self.import_graph = {}
        self.import_map = {}
        self.known_internal_modules = set()

    def build(self) -> Dict[str, Set[str]]:
        """Build and return the import graph.

        Returns:
            Dependency graph as an adjacency list.
        """
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

            importable = get_importable_path(path)
            if importable:
                self.import_map[importable] = path
                self.known_internal_modules.add(importable)

    def _resolve_imports(self):
        """Iterate through modules and resolve their imports to project files."""
        for module in self.modules_data:
            source_path = module.get("path", "")
            if not source_path:
                continue

            for imp in module.get("imports", []):
                target = resolve_import(imp, self.import_map)
                if target and target != source_path:
                    self.import_graph[source_path].add(target)
