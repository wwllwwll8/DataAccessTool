# Data Access Tool TODO

Build a unified data gateway that shields backend data formats (SQL, JSON/document, Graph) behind one agent-friendly interface.

## Project Rules (Mandatory)
- Implementation language/runtime: **Python `3.12+`**.
- Development methodology: **TDD only** (Red -> Green -> Refactor).
- Every feature task must start with failing tests, then minimal implementation, then refactor.
- CI must run full test suite and block merge on failing tests.

## Epic 0: Project Foundation (Python + TDD)

### [x] Task 0.1: Bootstrap Python 3.12+ project
- **Acceptance criteria**
- Project metadata and tooling explicitly pin/support Python `3.12+`.
- Virtual environment and dependency workflow documented.
- Baseline project layout created (`src/`, `tests/`, config files).

### [x] Task 0.2: Set up test stack and TDD guardrails
- **Acceptance criteria**
- Test framework configured (unit + integration markers).
- Coverage reporting enabled with minimum threshold.
- Pre-commit/CI checks enforce tests and prevent merge on failures.

### [x] Task 0.3: Define TDD contribution workflow
- **Acceptance criteria**
- CONTRIBUTING docs require Red->Green->Refactor cycle.
- PR template includes "failing test first" checklist item.
- Example test-first implementation flow documented.

## Epic 1: Core Contract (Unified Interface)

### [x] Task 1.1: Define canonical request/response models
- **Acceptance criteria**
- Types exist for `QueryRequest`, `InsertRequest`, `UpdateRequest`.
- Shared response envelope includes `data`, `meta`, `errors`.
- Paging/filter/sort fields are backend-agnostic.

### [x] Task 1.2: Define query DSL/AST
- **Acceptance criteria**
- DSL supports select fields, filters, sort, limit/offset (or cursor).
- No backend-native syntax leaks into public API.
- Validation errors returned for unsupported expressions.

### [x] Task 1.3: Publish interface spec
- **Acceptance criteria**
- Single interface documented (`query`, `insert`, `update`).
- Example payloads for SQL/JSON/Graph use same API shape.
- Versioning strategy (`v1`) documented.

## Epic 2: Adapter Framework

### [x] Task 2.1: Create adapter base contract
- **Acceptance criteria**
- Adapter interface includes `connect`, `query`, `insert`, `update`, `healthCheck`, `close`.
- Capability flags supported (e.g. transactions, graph traversal).
- Unit tests cover adapter lifecycle.

### [x] Task 2.2: Build translation pipeline
- **Acceptance criteria**
- Canonical AST converts to backend-native command via pluggable translator.
- Reverse mapping normalizes native results to canonical response.
- Translator errors map to unified error codes.

### [x] Task 2.3: Build adapter registry
- **Acceptance criteria**
- Backends register by key (`sql`, `json`, `graph`).
- Runtime can route request to configured adapter.
- Unknown adapter returns typed “unsupported backend” error.

## Epic 3: SQL Adapter (First Production Path)

### [x] Task 3.1: Implement SQL query translator
- **Acceptance criteria**
- Supports basic select/filter/sort/pagination.
- Uses parameterized queries only.
- Rejects unsupported DSL features with clear errors.

### Task 3.2: Implement SQL insert/update
- **Acceptance criteria**
- Insert supports single + batch rows.
- Update supports filtered updates with affected row count.
- Optional transaction wrapper supported per request.

### Task 3.3: SQL integration tests
- **Acceptance criteria**
- Tests run against real DB container.
- Golden tests validate request->SQL and SQL->response mapping.
- Failure cases tested (constraint violation, timeout, disconnect).

## Epic 4: JSON/Document Adapter

### Task 4.1: Define JSON storage strategy
- **Acceptance criteria**
- Document identity and indexing approach documented.
- Filter semantics aligned with canonical DSL.
- Merge/replace behavior defined for updates.

### Task 4.2: Implement query/insert/update
- **Acceptance criteria**
- Same public interface as SQL path.
- Deterministic result ordering for tests.
- Concurrency strategy documented (locking/versioning).

### Task 4.3: Conformance tests
- **Acceptance criteria**
- Shared adapter test suite passes for JSON adapter.
- Behavior matches canonical spec for core operations.

## Epic 5: Graph Adapter

### Task 5.1: Map canonical model to graph model
- **Acceptance criteria**
- Node/edge and relation mapping documented.
- Query DSL subset for graph traversal is defined.
- Unsupported operations are explicitly flagged.

### Task 5.2: Implement graph query/insert/update
- **Acceptance criteria**
- Query supports node filters and basic relation traversal.
- Insert/update supports node and relation updates.
- Responses normalized to canonical shape.

### Task 5.3: Graph integration tests
- **Acceptance criteria**
- Seed graph fixtures and validate traversal outputs.
- Error mapping validated for graph-native failures.

## Epic 6: Cross-Cutting Reliability/Security

### Task 6.1: Unified error taxonomy
- **Acceptance criteria**
- Error codes: validation/authz/timeout/conflict/not-found/unsupported/internal.
- All adapters map native errors into taxonomy.
- Error responses include machine code + safe message.

### Task 6.2: Security controls
- **Acceptance criteria**
- AuthN/AuthZ middleware enforced before adapter calls.
- Field/table/entity allowlist supported.
- Audit log emitted for insert/update operations.

### Task 6.3: Resilience controls
- **Acceptance criteria**
- Timeouts, retries, and circuit-breaker policies configurable per adapter.
- Health check endpoint reports adapter readiness.
- Graceful degradation behavior documented.

## Epic 7: Observability + Agent Tooling

### Task 7.1: Metrics and tracing
- **Acceptance criteria**
- Latency/error/throughput metrics by adapter and operation.
- Trace spans cover request->translation->backend call.
- Correlation ID included in logs and responses.

### Task 7.2: Agent-facing tool schema
- **Acceptance criteria**
- Tool inputs mirror canonical API and are strongly validated.
- Guardrails: max rows, forbidden fields, operation policy.
- Stable output schema optimized for LLM consumption.

### Task 7.3: Usage examples
- **Acceptance criteria**
- End-to-end examples for query/insert/update from an agent.
- Docs include safe prompts and anti-patterns.

## Epic 8: Release Readiness

### Task 8.1: Developer docs
- **Acceptance criteria**
- “How to add a new adapter” guide.
- API reference with sample payloads and errors.
- Local run + test instructions complete.

### Task 8.2: Production checklist
- **Acceptance criteria**
- Config/env var matrix documented.
- Backup/recovery and rollback plan documented.
- SLOs and alerts defined.

### Task 8.3: v1 cut
- **Acceptance criteria**
- SQL + JSON adapters GA (graph optional beta).
- Conformance + integration suites green in CI.
- Version tag and changelog published.

## Suggested Priority
- `P0`: Epic 1, 2, 3, 6.1
- `P1`: Epic 4, 7.1, 7.2
- `P2`: Epic 5, 8
