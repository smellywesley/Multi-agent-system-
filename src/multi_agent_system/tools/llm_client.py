import os
import time
from typing import Any, Optional, Type
from pydantic import BaseModel
from google import genai
from google.genai import types
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        """
        Gold Standard 2026 Client.
        """
        # Resolve keys
        self.gemini_key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY")
        self.sambanova_key = getattr(settings, "SAMBANOVA_API_KEY", None) or os.environ.get("SAMBANOVA_API_KEY")
        
        # ⚡ 2026 STABLE MODELS (These replace the retired 1.5/2.0 series)
        self.gemini_model = "gemini-2.0-flash" 
        self.samba_model = "Meta-Llama-3.3-70B-Instruct"
        
        self.genai_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None
        self.samba_client = openai.OpenAI(
            api_key=self.sambanova_key,
            base_url="https://api.sambanova.ai/v1",
        ) if self.sambanova_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
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
            print(f"SambaNova busy, falling back: {str(e)}")
            time.sleep(1)

        # Fallback to Gemini 2.0
        if not self.genai_client:
            raise ValueError("API Keys missing in Render Environment.")
            
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
            # If 2.0 Flash fails, try the generic 'gemini-flash' alias as a last resort
            response = self.genai_client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            return response.parsed
