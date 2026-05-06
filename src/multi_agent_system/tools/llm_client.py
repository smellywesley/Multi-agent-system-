"""Placeholder LLM client interface."""

from multi_agent_system.config import Settings


class LLMClient:
    """Lightweight, mock-friendly LLM client placeholder."""

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model

    def generate(self, prompt: str) -> str:
        """Return deterministic placeholder output for now."""
        return f"[{self.model}] {prompt}"
