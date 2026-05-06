"""Vercel entrypoint exposing the FastAPI ASGI app."""

from multi_agent_system.api import app

__all__ = ["app"]
