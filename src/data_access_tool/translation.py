"""Canonical translation interfaces for backend execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from data_access_tool.models import ErrorDetail, ResponseEnvelope
from data_access_tool.query_ast import QueryAST


@dataclass(frozen=True)
class NativeCommand:
    """Backend-native command payload produced by translators."""

    command: str
    params: dict[str, Any] = field(default_factory=dict)


class Translator(Protocol):
    """Translator contract from canonical AST to native command."""

    def to_native(self, ast: QueryAST) -> NativeCommand:
        """Convert canonical AST to backend-native command."""


def normalize_result(rows: list[dict[str, Any]], *, count: int | None = None) -> ResponseEnvelope:
    """Normalize native backend rows into the canonical response envelope."""
    meta: dict[str, Any] = {}
    if count is not None:
        meta["count"] = count
    return ResponseEnvelope(data=tuple(rows), meta=meta, errors=())


def normalize_error(code: str, message: str) -> ResponseEnvelope:
    """Normalize backend errors into canonical response errors."""
    return ResponseEnvelope(
        data=(),
        meta={},
        errors=(ErrorDetail(code=code, message=message),),
    )
