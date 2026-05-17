"""Tests for SQL query translator."""

import pytest

from data_access_tool.query_ast import FilterCondition, FilterOperator, QueryAST, SortField
from data_access_tool.sql_translator import SqlQueryTranslator


@pytest.mark.unit
def test_sql_translator_builds_select_filter_sort_and_pagination() -> None:
    translator = SqlQueryTranslator()
    ast = QueryAST(
        source="users",
        select=("id", "name"),
        filters=(
            FilterCondition(field="age", op=FilterOperator.GTE, value=18),
            FilterCondition(field="status", op=FilterOperator.EQ, value="active"),
        ),
        sort=(SortField(field="name"), SortField(field="created_at", descending=True)),
        limit=50,
        offset=10,
    )

    command = translator.to_native(ast)

    assert command.command == (
        "SELECT id, name FROM users "
        "WHERE age >= :p0 AND status = :p1 "
        "ORDER BY name ASC, created_at DESC "
        "LIMIT :limit OFFSET :offset"
    )
    assert command.params == {"p0": 18, "p1": "active", "limit": 50, "offset": 10}


@pytest.mark.unit
def test_sql_translator_uses_parameterized_values() -> None:
    translator = SqlQueryTranslator()
    ast = QueryAST(
        source="users",
        select=("id",),
        filters=(FilterCondition(field="name", op=FilterOperator.EQ, value="Alice"),),
        sort=(),
        limit=10,
        offset=0,
    )

    command = translator.to_native(ast)

    assert "Alice" not in command.command
    assert ":p0" in command.command
    assert command.params["p0"] == "Alice"


@pytest.mark.unit
def test_sql_translator_rejects_invalid_identifier() -> None:
    translator = SqlQueryTranslator()
    ast = QueryAST(
        source="users",
        select=("id",),
        filters=(FilterCondition(field="name;DROP", op=FilterOperator.EQ, value="Alice"),),
        sort=(),
        limit=10,
        offset=0,
    )

    with pytest.raises(ValueError, match="invalid identifier"):
        translator.to_native(ast)
