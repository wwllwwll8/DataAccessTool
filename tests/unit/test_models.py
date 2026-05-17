"""Tests for canonical request/response models."""

import pytest

from data_access_tool.models import (
    ErrorDetail,
    InsertRequest,
    QueryRequest,
    ResponseEnvelope,
    UpdateRequest,
)


@pytest.mark.unit
def test_query_request_defaults() -> None:
    request = QueryRequest(source="users")

    assert request.source == "users"
    assert request.select == ()
    assert request.filters == {}
    assert request.sort == ()
    assert request.limit == 100
    assert request.offset == 0


@pytest.mark.unit
def test_query_request_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError, match="limit must be greater than 0"):
        QueryRequest(source="users", limit=0)


@pytest.mark.unit
def test_insert_request_requires_records() -> None:
    with pytest.raises(ValueError, match="records cannot be empty"):
        InsertRequest(source="users", records=())


@pytest.mark.unit
def test_update_request_requires_values() -> None:
    with pytest.raises(ValueError, match="values cannot be empty"):
        UpdateRequest(source="users", filters={"id": 1}, values={})


@pytest.mark.unit
def test_response_envelope_shape() -> None:
    response = ResponseEnvelope(
        data=({"id": 1, "name": "Alice"},),
        meta={"count": 1},
        errors=(ErrorDetail(code="none", message=""),),
    )

    assert response.data[0]["name"] == "Alice"
    assert response.meta["count"] == 1
    assert response.errors[0].code == "none"
