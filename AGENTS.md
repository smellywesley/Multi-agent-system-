# AGENTS.md

## Purpose

This repository provides a production-ready scaffold for a modular Python multi-agent system.
The current focus is architecture and extensibility, not heavyweight LLM behavior.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `python -m pip install -e ".[dev]"`
3. Copy environment template:
   - `cp .env.example .env`

## Commands

- Show CLI help:
  - `multi-agent-system --help`
- Run example workflow:
  - `multi-agent-system run --task "Your task"`
- Lint:
  - `ruff check .`
- Type check:
  - `mypy src/multi_agent_system`
- Test:
  - `pytest -v`

## Coding conventions

- Python 3.10+
- Use `src/` package layout
- Add explicit type hints for all public functions and methods
- Keep modules focused and small
- Prefer composition and protocol-like abstractions over tightly coupled code
- Use Pydantic v2 models for structured messages/settings
- Use `structlog` for structured logging and observability context
- Avoid real external API calls in tests; mock boundaries

## Testing expectations

- Every new feature should include tests under `tests/`
- Tests must run offline and deterministically
- `pytest -v` should pass before commit

## Deployment expectations

- Container image should run as a non-root user
- Configuration comes from environment variables
- Runtime logs should be structured and machine-readable
- CI should run lint + type checks + tests before release
