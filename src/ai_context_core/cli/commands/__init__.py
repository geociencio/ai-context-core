"""CLI command groups package."""

from .base import init_cmd, stats_cmd, clean_cmd, serve_cmd, profiles_cmd
from .analysis import analyze_cmd, audit_cmd, inspect_cmd
from .reports import patterns_cmd, security_cmd, help_me_cmd
from .specialized import deps_cmd, git_cmd, qgis_cmd
from ..interactive import interactive_cmd
from .workflows import full_scan_cmd
from .maintenance import (
    doctor_cmd,
    fix_cmd,
    graph_cmd,
    compare_cmd,
    scaffold_cmd,
    roadmap_cmd,
)

# Export lists for easier registration
BASE_CMDS = [init_cmd, stats_cmd, clean_cmd, serve_cmd, profiles_cmd]
ANALYSIS_CMDS = [analyze_cmd, audit_cmd, inspect_cmd]
REPORT_CMDS = [patterns_cmd, security_cmd, help_me_cmd]
SPECIALIZED_CMDS = [deps_cmd, git_cmd, qgis_cmd]
INTERACTIVE_CMDS = [interactive_cmd]
WORKFLOW_CMDS = [full_scan_cmd]
MAINTENANCE_CMDS = [
    doctor_cmd,
    fix_cmd,
    graph_cmd,
    compare_cmd,
    scaffold_cmd,
    roadmap_cmd,
]

ALL_CMDS = (
    BASE_CMDS
    + ANALYSIS_CMDS
    + REPORT_CMDS
    + SPECIALIZED_CMDS
    + INTERACTIVE_CMDS
    + WORKFLOW_CMDS
    + MAINTENANCE_CMDS
)
