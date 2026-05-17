"""SQL translator for canonical query AST."""

from __future__ import annotations

import re

from data_access_tool.query_ast import FilterOperator, QueryAST
from data_access_tool.translation import NativeCommand

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class SqlQueryTranslator:
    """Translate canonical QueryAST into parameterized SQL."""

    def to_native(self, ast: QueryAST) -> NativeCommand:
        ast.validate()
        self._validate_identifiers(ast)

        params: dict[str, object] = {}
        selected = "*" if not ast.select else ", ".join(ast.select)
        query = f"SELECT {selected} FROM {ast.source}"

        if ast.filters:
            where_parts: list[str] = []
            for index, condition in enumerate(ast.filters):
                key = f"p{index}"
                if condition.op == FilterOperator.IN:
                    if not isinstance(condition.value, (list, tuple)):
                        raise ValueError("IN operator expects list or tuple")
                    placeholders: list[str] = []
                    for in_index, in_value in enumerate(condition.value):
                        in_key = f"{key}_{in_index}"
                        placeholders.append(f":{in_key}")
                        params[in_key] = in_value
                    where_parts.append(f"{condition.field} IN ({', '.join(placeholders)})")
                else:
                    where_parts.append(f"{condition.field} {self._op_sql(condition.op)} :{key}")
                    params[key] = condition.value
            query += f" WHERE {' AND '.join(where_parts)}"

        if ast.sort:
            sort_parts = [
                f"{item.field} {'DESC' if item.descending else 'ASC'}"
                for item in ast.sort
            ]
            query += f" ORDER BY {', '.join(sort_parts)}"

        params["limit"] = ast.limit
        params["offset"] = ast.offset
        query += " LIMIT :limit OFFSET :offset"
        return NativeCommand(command=query, params=params)

    def _validate_identifiers(self, ast: QueryAST) -> None:
        identifiers = [ast.source, *ast.select]
        identifiers.extend(item.field for item in ast.filters)
        identifiers.extend(item.field for item in ast.sort)
        for identifier in identifiers:
            if not _IDENTIFIER_RE.match(identifier):
                raise ValueError(f"invalid identifier: {identifier}")

    @staticmethod
    def _op_sql(operator: FilterOperator) -> str:
        mapping = {
            FilterOperator.EQ: "=",
            FilterOperator.NE: "!=",
            FilterOperator.GT: ">",
            FilterOperator.GTE: ">=",
            FilterOperator.LT: "<",
            FilterOperator.LTE: "<=",
        }
        try:
            return mapping[operator]
        except KeyError as exc:
            raise ValueError(f"unsupported operator: {operator}") from exc
