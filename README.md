# Multi Agent System

A clean, production-ready scaffold for a modular Python multi-agent system.

## Features

- `src/` layout with typed Python package: `multi_agent_system`
- Orchestrator/manager and specialist agent architecture
- Pydantic v2 settings and schemas
- Structured logging with `structlog`
- CLI entry point: `multi-agent-system`
- Tool and workflow separation for extensibility
- Quality tooling: `pytest`, `ruff`, and `mypy`
- Dockerfile and docker-compose setup

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
multi-agent-system --help
```

## Run

```bash
multi-agent-system run --task "Review this document"
```

## Development checks

```bash
ruff check .
mypy src/multi_agent_system
pytest -v
```
