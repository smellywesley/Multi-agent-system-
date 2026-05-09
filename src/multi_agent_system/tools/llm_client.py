import os
import time
from typing import Any, Optional, Type
from pydantic import BaseModel
from google import genai
from google.genai import types
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        # 1. Resolve API Keys from Render Env
        self.gemini_key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY")
        self.sambanova_key = getattr(settings, "SAMBANOVA_API_KEY", None) or os.environ.get("SAMBANOVA_API_KEY")
        
        # 2. 2026 STABLE MODEL IDENTIFIERS
        self.gemini_model = "gemini-3-flash" # Replaces the retired 1.5/2.0 series
        self.samba_model = "Meta-Llama-3.3-70B-Instruct" # Replaces the retired 405B
        
        # 3. Initialize Clients
        self.genai_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None
        self.samba_client = openai.OpenAI(
            api_key=self.sambanova_key,
            base_url="https://api.sambanova.ai/v1",
        ) if self.sambanova_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        """Professional extraction with 2026-native models."""
        # --- Attempt 1: SambaNova (Llama 3.3) ---
        try:
            if self.samba_client:
                response = self.samba_client.chat.completions.create(
                    model=self.samba_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            print(f"SambaNova busy/retired, falling back: {str(e)}")
            time.sleep(1)

        # --- Attempt 2: Gemini 3 Flash Fallback ---
        if not self.genai_client:
            raise ValueError("No AI providers configured. Verify keys in Render Environment.")
            
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
            # Final retry logic for 2026 API stability
            time.sleep(2)
            response = self.genai_client.models.generate_content(
                model=self.gemini_model, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=schema)
            )
            return response.parsed
