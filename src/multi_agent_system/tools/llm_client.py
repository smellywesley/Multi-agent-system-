"""Google Gemini-backed LLM client."""

from typing import TypeVar, cast

from google import genai
from google.genai import types
from pydantic import BaseModel

from multi_agent_system.config import Settings

TModel = TypeVar("TModel", bound=BaseModel)


class LLMClient:
    """Wrapper around Google GenAI SDK with schema-constrained output parsing."""

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_structured(self, prompt: str, schema: type[TModel]) -> TModel:
        """Generate and parse structured output into the provided Pydantic schema."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        parsed = response.parsed
        if parsed is None:
            raise ValueError("Gemini returned no parsed structured response")
        return cast(TModel, parsed)
