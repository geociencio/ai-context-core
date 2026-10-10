"""Rich ``Console``/``Table`` with a dependency-free fallback.

Centralizes the optional-``rich`` handling so commands don't repeat the
try/except stub block.
"""

try:  # pragma: no cover - exercised only when rich is installed
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - graceful degradation without rich

    class Console:  # type: ignore[no-redef]
        """Minimal stdout fallback for :class:`rich.console.Console`."""

        def print(self, *args, **kwargs) -> None:
            print(*args)

    class Table:  # type: ignore[no-redef]
        """No-op fallback for :class:`rich.table.Table`."""

        def __init__(self, *args, **kwargs) -> None:
            pass

        def add_column(self, *args, **kwargs) -> None:
            pass

        def add_row(self, *args, **kwargs) -> None:
            pass


__all__ = ["Console", "Table"]
