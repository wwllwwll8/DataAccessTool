# Contributing

## Runtime
- Use Python `3.12+`.
- Recommended setup:
  - `python3.12 -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install --upgrade pip`
  - `python -m pip install -e ".[dev]"`

## Development Workflow (TDD Required)
Follow Red -> Green -> Refactor for every feature and bugfix.

1. **Red**: Write or update a test that fails for the desired behavior.
2. **Green**: Implement the smallest code change that makes the test pass.
3. **Refactor**: Improve code quality while keeping tests green.

Do not merge work that skips the red step.

## Running checks
- `python -m ruff check .`
- `python -m mypy src`
- `python -m pytest`

## Pre-commit
- Install hooks: `pre-commit install`
- Run all hooks: `pre-commit run --all-files`
