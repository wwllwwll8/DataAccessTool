# Data Access Tool API Spec (v1)

## Version
- `v1`

## Public Operations
- `query(request: QueryRequest) -> ResponseEnvelope`
- `insert(request: InsertRequest) -> ResponseEnvelope`
- `update(request: UpdateRequest) -> ResponseEnvelope`

## Canonical Request Models

### QueryRequest
- `source: str` - logical collection/table/node set name
- `select: tuple[str, ...]` - field names only
- `filters: dict[str, Any]` - backend-agnostic filter object
- `sort: tuple[str, ...]` - canonical sort expressions
- `limit: int` - result size limit, `> 0`
- `offset: int` - pagination offset, `>= 0`

### InsertRequest
- `source: str`
- `records: tuple[dict[str, Any], ...]` - one or more records

### UpdateRequest
- `source: str`
- `filters: dict[str, Any]`
- `values: dict[str, Any]` - fields to update

## Canonical Response Model
`ResponseEnvelope`
- `data: tuple[dict[str, Any], ...]`
- `meta: dict[str, Any]`
- `errors: tuple[ErrorDetail, ...]`

`ErrorDetail`
- `code: str`
- `message: str`

## Backend Agnostic DSL
- Query expressions must use canonical names and operators.
- Backend syntax (raw SQL, graph pattern syntax, JSON query language) is not allowed in the public interface.
- Use `QueryAST`, `FilterCondition`, and `SortField` as the neutral AST model.

## Example Shapes (same API, different targets)
- SQL target: `source="users"`
- JSON target: `source="users_documents"`
- Graph target: `source="user_nodes"`

Each backend receives the same request object shape through adapters.
