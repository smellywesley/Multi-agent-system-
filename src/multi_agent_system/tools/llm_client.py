import os
import time
from typing import Any, Type
from pydantic import BaseModel
import openai

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        # Resolve keys from Render Environment
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.samba_key = os.environ.get("SAMBANOVA_API_KEY")
        
        # 2026 Stable Models
        self.primary_model = "llama-3.3-70b-versatile"
        self.backup_model = "Meta-Llama-3.3-70B-Instruct"
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
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
            print(f"Groq error: {str(e)}")
            time.sleep(1)
        
        # Final Fallback to SambaNova
        response = self.samba_client.chat.completions.create(
            model=self.backup_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return schema.model_validate_json(response.choices[0].message.content)
