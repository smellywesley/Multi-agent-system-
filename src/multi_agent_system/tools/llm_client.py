import os
from typing import Any, Optional, Type
from pydantic import BaseModel
from google import genai
from google.genai import types
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        """
        Initialize LLM Client. 
        Accepts 'settings' for framework compatibility, but falls back 
        to environment variables for standalone use.
        """
        # Pull keys from settings object if it exists, otherwise check environment
        self.gemini_key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY")
        self.sambanova_key = getattr(settings, "SAMBANOVA_API_KEY", None) or os.environ.get("SAMBANOVA_API_KEY")
        
        # Standardize on the high-quota stable model
        self.gemini_model = "gemini-1.5-flash-latest"
        
        self.genai_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None
        self.samba_client = openai.OpenAI(
            api_key=self.sambanova_key,
            base_url="https://api.sambanova.ai/v1",
        ) if self.sambanova_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        """Generate structured output with SambaNova or Gemini fallback."""
        try:
            if self.samba_client:
                response = self.samba_client.chat.completions.create(
                    model="Meta-Llama-3.1-405B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            print(f"SambaNova primary failed, falling back to Gemini: {str(e)}")

        if not self.genai_client:
            raise ValueError("LLM Clients uninitialized. Please provide GEMINI_API_KEY.")
            
        response = self.genai_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return response.parsed
