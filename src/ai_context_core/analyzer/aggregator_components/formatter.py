"""Formatting logic for project-level complexity aggregation."""

from typing import List, Dict, Any

def format_complexity_agg(valid_modules: List[Dict[str, Any]], project_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Builds the complexity aggregation dictionary for backward compatibility."""
    return {
        "total_modules": len(valid_modules),
        "total_lines": project_metrics.get("total_lines_code", 0),
        "total_physical_lines": project_metrics.get("total_physical_lines", 0),
        "total_functions": project_metrics.get("total_functions", 0),
        "total_classes": project_metrics.get("total_classes", 0),
        "average_complexity": project_metrics.get("average_complexity", 0),
        "avg_maintenance_index": project_metrics.get("avg_maintenance_index", 0),
        "most_complex_modules": sorted(
            [(m["path"], m.get("complexity", 0)) for m in valid_modules],
            key=lambda x: x[1],
            reverse=True,
        )[:10],
    }
