"""Multi-provider LLM client (Gemini, SambaNova, Ollama)."""

from typing import Any, TypeVar, cast

from google import genai
from google.genai import types
from openai import OpenAI
from pydantic import BaseModel

from multi_agent_system.config import Settings

TModel = TypeVar("TModel", bound=BaseModel)


class LLMClient:
    """Switchboard client for Gemini and OpenAI-compatible providers."""

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.provider = settings.llm_provider.strip().lower()

        if self.provider == "gemini":
            self.gemini_client: genai.Client | None = genai.Client(api_key=settings.gemini_api_key)
            self.openai_client: OpenAI | None = None
        elif self.provider == "sambanova":
            self.gemini_client = None
            self.openai_client = OpenAI(
                api_key=settings.sambanova_api_key,
                base_url=settings.openai_base_url,
            )
        elif self.provider == "ollama":
            self.gemini_client = None
            self.openai_client = OpenAI(
                api_key="ollama",
                base_url="http://localhost:11434/v1",
            )
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")

    def generate_structured(self, prompt: str, schema: type[TModel]) -> TModel:
        """Generate and parse structured output into the provided Pydantic schema."""
        if self.provider == "gemini":
            if self.gemini_client is None:
                raise ValueError("Gemini client was not initialized")
            response = self.gemini_client.models.generate_content(
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

        if self.openai_client is None:
            raise ValueError("OpenAI-compatible client was not initialized")

        completion = self.openai_client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format=schema,
        )
        message: Any = completion.choices[0].message
        parsed = message.parsed
        if parsed is None:
            raise ValueError("Provider returned no parsed structured response")
        return cast(TModel, parsed)
