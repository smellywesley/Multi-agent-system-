import os
import time
from typing import Any, Optional, Type
from pydantic import BaseModel
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        """
        2026 Open-Source Gold Standard.
        Uses Groq (Primary) and SambaNova (Backup). No Gemini, no 404s.
        """
        self.groq_key = getattr(settings, "GROQ_API_KEY", None) or os.environ.get("GROQ_API_KEY")
        self.samba_key = getattr(settings, "SAMBANOVA_API_KEY", None) or os.environ.get("SAMBANOVA_API_KEY")
        
        # 2026 Open-Source Kings
        self.primary_model = "llama-3.3-70b-versatile" # Groq's high-speed workhorse
        self.backup_model = "Meta-Llama-3.3-70B-Instruct" # SambaNova's stable model
        
        self.groq_client = openai.OpenAI(
            api_key=self.groq_key,
            base_url="https://api.groq.com/openai/v1",
        ) if self.groq_key else None
        
        self.samba_client = openai.OpenAI(
            api_key=self.samba_key,
            base_url="https://api.sambanova.ai/v1",
        ) if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        """Structured extraction using pure Open-Source logic."""
        # --- Attempt 1: Groq (The Speed King) ---
        try:
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model=self.primary_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            print(f"Groq busy, falling back to SambaNova: {str(e)}")
            time.sleep(1)

        # --- Attempt 2: SambaNova (The Reliable Backup) ---
        if not self.samba_client:
            raise ValueError("No AI providers available. Ensure GROQ_API_KEY or SAMBANOVA_API_KEY is in Render.")
            
        try:
            response = self.samba_client.chat.completions.create(
                model=self.backup_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            raise RuntimeError(f"All open-source providers failed. Error: {str(e)}")
