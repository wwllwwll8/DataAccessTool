"""Tests for query AST DSL."""

import pytest

from data_access_tool.query_ast import FilterCondition, FilterOperator, QueryAST, SortField


@pytest.mark.unit
def test_query_ast_accepts_valid_input() -> None:
    ast = QueryAST(
        source="users",
        select=("id", "name"),
        filters=(FilterCondition(field="age", op=FilterOperator.GTE, value=18),),
        sort=(SortField(field="name"),),
        limit=25,
        offset=0,
    )

    ast.validate()


@pytest.mark.unit
def test_query_ast_rejects_backend_specific_select_syntax() -> None:
    ast = QueryAST(
        source="users",
        select=("SELECT * FROM users",),
        filters=(),
        sort=(),
        limit=10,
        offset=0,
    )

    with pytest.raises(ValueError, match="canonical names only"):
        ast.validate()


@pytest.mark.unit
def test_query_ast_rejects_invalid_limit() -> None:
    ast = QueryAST(
        source="users",
        select=(),
        filters=(),
        sort=(),
        limit=0,
        offset=0,
    )

    with pytest.raises(ValueError, match="limit must be greater than 0"):
        ast.validate()
