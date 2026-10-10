"""CLI command groups package (context-only surface, v5.0.0)."""

from .base import init_cmd, stats_cmd, clean_cmd, profiles_cmd
from .analysis import analyze_cmd, context_cmd
from .reports import help_me_cmd
from .specialized import deps_cmd, git_cmd
from .maintenance import graph_cmd, compare_cmd, roadmap_cmd
from .deprecated import DEPRECATED_CMDS

# Export lists for easier registration
BASE_CMDS = [init_cmd, stats_cmd, clean_cmd, profiles_cmd]
ANALYSIS_CMDS = [analyze_cmd, context_cmd]
REPORT_CMDS = [help_me_cmd]
SPECIALIZED_CMDS = [deps_cmd, git_cmd]
MAINTENANCE_CMDS = [graph_cmd, compare_cmd, roadmap_cmd]

ALL_CMDS = (
    BASE_CMDS + ANALYSIS_CMDS + REPORT_CMDS + SPECIALIZED_CMDS + MAINTENANCE_CMDS + DEPRECATED_CMDS
)
