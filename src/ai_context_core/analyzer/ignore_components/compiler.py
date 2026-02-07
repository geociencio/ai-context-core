"""Logic for compiling glob patterns into efficient Regex."""

import re
import fnmatch
from typing import List, Optional

def compile_ignore_patterns(patterns: List[str]) -> Optional[re.Pattern]:
    """Compiles glob patterns into a single regex."""
    if not patterns:
        return None
        
    regex_parts = []
    for p in patterns:
        part = fnmatch.translate(p.rstrip("/"))
        regex_parts.append(part)
        
    return re.compile("|".join(regex_parts))
