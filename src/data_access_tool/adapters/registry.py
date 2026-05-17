"""Adapter registration and retrieval."""

from __future__ import annotations

from dataclasses import dataclass, field

from data_access_tool.adapters.base import DataAdapter


@dataclass
class AdapterRegistry:
    _adapters: dict[str, DataAdapter] = field(default_factory=dict)

    def register(self, key: str, adapter: DataAdapter) -> None:
        if not key:
            raise ValueError("adapter key is required")
        self._adapters[key] = adapter

    def get(self, key: str) -> DataAdapter:
        try:
            return self._adapters[key]
        except KeyError as exc:
            raise LookupError(f"unsupported backend: {key}") from exc

    def list_backends(self) -> tuple[str, ...]:
        return tuple(sorted(self._adapters))
