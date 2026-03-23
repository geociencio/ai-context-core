"""AI Context Core Package"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("ai-context-core")
except importlib.metadata.PackageNotFoundError:
    # Versión de fallback durante desarrollo local (opcional)
    __version__ = "3.3.0"
