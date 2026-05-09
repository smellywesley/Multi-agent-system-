import os
from typing import Any, Optional, Type
from pydantic import BaseModel
from google import genai
from google.genai import types
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        """
        Gold Standard Initialization.
        Grabs keys from 'settings' object OR environment variables.
        """
        # 1. Resolve API Keys
        self.gemini_key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY")
        self.sambanova_key = getattr(settings, "SAMBANOVA_API_KEY", None) or os.environ.get("SAMBANOVA_API_KEY")
        
        # 2. Use stable identifiers for 2026
        # Gemini 1.5 Flash is the high-quota workhorse
        self.gemini_model = "gemini-1.5-flash"
        # Llama 3.3 70B is the current SambaNova stable replacement for 405B
        self.samba_model = "Meta-Llama-3.3-70B-Instruct"
        
        # 3. Initialize Clients
        self.genai_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None
        self.samba_client = openai.OpenAI(
            api_key=self.sambanova_key,
            base_url="https://api.sambanova.ai/v1",
        ) if self.sambanova_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        """Professional LLM handler with SambaNova primary and Gemini fallback."""
        # Try SambaNova first
        try:
            if self.samba_client:
                response = self.samba_client.chat.completions.create(
                    model=self.samba_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            print(f"SambaNova primary failed, falling back to Gemini: {str(e)}")

        # Fallback to Gemini 1.5 Flash
        if not self.genai_client:
            raise ValueError("No LLM clients available. Ensure GEMINI_API_KEY is in Render environment.")
            
        try:
            response = self.genai_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            return response.parsed
        except Exception as e:
            # Final security capture to prevent public tracebacks
            raise RuntimeError(f"All AI providers failed. Check API limits/keys. Error: {str(e)}")
