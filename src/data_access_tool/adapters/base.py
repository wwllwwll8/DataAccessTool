"""Core adapter contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from data_access_tool.models import InsertRequest, QueryRequest, ResponseEnvelope, UpdateRequest


@dataclass(frozen=True)
class AdapterCapabilities:
    transactions: bool = False
    graph_traversal: bool = False


class DataAdapter(Protocol):
    """Contract every backend adapter must satisfy."""

    capabilities: AdapterCapabilities

    def connect(self) -> None:
        """Open underlying connection(s)."""

    def health_check(self) -> bool:
        """Return readiness state for this adapter."""

    def close(self) -> None:
        """Close underlying connection(s)."""

    def query(self, request: QueryRequest) -> ResponseEnvelope:
        """Execute backend query from canonical request."""

    def insert(self, request: InsertRequest) -> ResponseEnvelope:
        """Execute backend insert from canonical request."""

    def update(self, request: UpdateRequest) -> ResponseEnvelope:
        """Execute backend update from canonical request."""
