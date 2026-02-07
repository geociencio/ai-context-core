"""Generic AST visitors for information extraction."""

import ast
from typing import List, Dict, Any, Optional


from .ast_visitors_components import (
    FunctionVisitor,
    extract_functions,
    ClassVisitor,
    extract_classes,
    DocstringVisitor,
    check_docstrings,
    ImportVisitor,
    extract_imports,
    detect_unused_imports
)
