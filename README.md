# DataAccessTool

Unified data access layer that provides one interface for query, insert, and update operations across SQL, JSON/document, and graph backends.

## Requirements
- Python `3.12+`

## Quick Start
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

## Development
- TDD is mandatory: Red -> Green -> Refactor.
- Read `CONTRIBUTING.md` for team workflow and checks.