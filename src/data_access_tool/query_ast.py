"""Backend-agnostic query AST for the public interface."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FilterOperator(str, Enum):
    """Supported canonical filter operators."""

    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"


@dataclass(frozen=True)
class FilterCondition:
    field: str
    op: FilterOperator
    value: object


@dataclass(frozen=True)
class SortField:
    field: str
    descending: bool = False


@dataclass(frozen=True)
class QueryAST:
    source: str
    select: tuple[str, ...]
    filters: tuple[FilterCondition, ...]
    sort: tuple[SortField, ...]
    limit: int
    offset: int

    def validate(self) -> None:
        """Validate AST values and reject backend-specific syntax leakage."""
        if not self.source:
            raise ValueError("source is required")
        if self.limit < 1:
            raise ValueError("limit must be greater than 0")
        if self.offset < 0:
            raise ValueError("offset must be >= 0")
        for name in self.select:
            if any(token in name.lower() for token in ("select ", "match ", "{", "}")):
                raise ValueError("select fields must be canonical names only")
