"""Tests for adapter contract support classes."""

import pytest

from data_access_tool.adapters.base import AdapterCapabilities
from data_access_tool.adapters.registry import AdapterRegistry
from data_access_tool.models import ErrorDetail
from data_access_tool.query_ast import FilterCondition, FilterOperator, QueryAST
from data_access_tool.translation import NativeCommand, normalize_error, normalize_result


class DummyAdapter:
    capabilities = AdapterCapabilities(transactions=True, graph_traversal=False)

    def connect(self) -> None:
        return None

    def health_check(self) -> bool:
        return True

    def close(self) -> None:
        return None

    def query(self, request):  # noqa: ANN001
        raise NotImplementedError

    def insert(self, request):  # noqa: ANN001
        raise NotImplementedError

    def update(self, request):  # noqa: ANN001
        raise NotImplementedError


@pytest.mark.unit
def test_registry_register_and_get() -> None:
    registry = AdapterRegistry()
    adapter = DummyAdapter()
    registry.register("sql", adapter)

    loaded = registry.get("sql")
    assert loaded is adapter
    assert registry.list_backends() == ("sql",)


@pytest.mark.unit
def test_registry_rejects_unknown_backend() -> None:
    registry = AdapterRegistry()
    with pytest.raises(LookupError, match="unsupported backend"):
        registry.get("graph")


@pytest.mark.unit
def test_normalize_result_creates_response_envelope() -> None:
    response = normalize_result([{"id": 1}], count=1)
    assert response.data[0]["id"] == 1
    assert response.meta["count"] == 1
    assert response.errors == ()


@pytest.mark.unit
def test_normalize_error_creates_error_response() -> None:
    response = normalize_error("timeout", "upstream timeout")
    assert response.data == ()
    assert response.meta == {}
    assert response.errors == (ErrorDetail(code="timeout", message="upstream timeout"),)


@pytest.mark.unit
def test_native_command_shape_and_ast_validation() -> None:
    command = NativeCommand(command="SELECT * FROM users", params={"limit": 10})
    assert command.command.startswith("SELECT")
    assert command.params["limit"] == 10

    ast = QueryAST(
        source="users",
        select=("id",),
        filters=(FilterCondition(field="id", op=FilterOperator.EQ, value=1),),
        sort=(),
        limit=10,
        offset=0,
    )
    ast.validate()
