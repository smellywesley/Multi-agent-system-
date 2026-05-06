"""OpenAI-backed LLM client."""

from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from multi_agent_system.config import Settings

TModel = TypeVar("TModel", bound=BaseModel)


class LLMClient:
    """Thin wrapper around OpenAI SDK with schema-constrained output parsing."""

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_structured(self, prompt: str, schema: type[TModel]) -> TModel:
        """Generate and parse structured output into the provided Pydantic schema."""
        response = self.client.responses.parse(
            model=self.model,
            input=[
                {"role": "system", "content": "Return only valid structured output."},
                {"role": "user", "content": prompt},
            ],
            text_format=schema,
        )
        return response.output_parsed
