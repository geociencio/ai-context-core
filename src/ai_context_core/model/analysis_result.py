"""Normalized, provenance-tagged analysis result.

The :class:`AnalysisResult` is the boundary type exchanged between *sources*
(the extraction layer) and the *context* transform/render layers. It deliberately
wraps the legacy analysis dictionary so that existing builders keep working while
provenance is tracked separately.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

SCHEMA_VERSION = 1


@dataclass
class Provenance:
    """Identity of the data producer for a given analysis result.

    Attributes:
        source: Source name (``"builtin"`` or ``"external"``).
        schema: Producer schema version (external) or the context schema.
        tool_version: Version of the producing tool.
        git_sha: Git revision of the analyzed project, when available.
    """

    source: str
    schema: Optional[Any] = None
    tool_version: Optional[str] = None
    git_sha: Optional[str] = None
    content_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Return the provenance as a plain dictionary."""
        return {
            "source": self.source,
            "schema": self.schema,
            "tool_version": self.tool_version,
            "git_sha": self.git_sha,
            "content_hash": self.content_hash,
        }


@dataclass
class AnalysisResult:
    """A normalized analysis payload plus its provenance.

    Attributes:
        data: Legacy-compatible analysis dictionary consumed by the builders.
        provenance: Producer identity for the payload.
    """

    data: Dict[str, Any] = field(default_factory=dict)
    provenance: Provenance = field(default_factory=lambda: Provenance(source="unknown"))

    def with_meta(self) -> Dict[str, Any]:
        """Return the payload with a ``_meta`` provenance block attached."""
        out = dict(self.data)
        out["_meta"] = {"schema": SCHEMA_VERSION, **self.provenance.to_dict()}
        return out
