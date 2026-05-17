"""Canonical request and response models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Record = dict[str, Any]
JSONLike = dict[str, Any]


@dataclass(frozen=True)
class QueryRequest:
    """Backend-agnostic query shape."""

    source: str
    select: tuple[str, ...] = ()
    filters: JSONLike = field(default_factory=dict)
    sort: tuple[str, ...] = ()
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError("limit must be greater than 0")
        if self.offset < 0:
            raise ValueError("offset must be >= 0")


@dataclass(frozen=True)
class InsertRequest:
    """Backend-agnostic insert shape."""

    source: str
    records: tuple[Record, ...]

    def __post_init__(self) -> None:
        if not self.records:
            raise ValueError("records cannot be empty")


@dataclass(frozen=True)
class UpdateRequest:
    """Backend-agnostic update shape."""

    source: str
    filters: JSONLike
    values: Record

    def __post_init__(self) -> None:
        if not self.values:
            raise ValueError("values cannot be empty")


@dataclass(frozen=True)
class ErrorDetail:
    """Unified error detail."""

    code: str
    message: str


@dataclass(frozen=True)
class ResponseEnvelope:
    """Unified response envelope for all operations."""

    data: tuple[Record, ...] = ()
    meta: JSONLike = field(default_factory=dict)
    errors: tuple[ErrorDetail, ...] = ()
