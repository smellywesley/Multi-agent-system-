import os
import time
import threading
from typing import Any, Type
from pydantic import BaseModel
import openai

# This lock prevents multiple agents from hitting the API at the exact same millisecond
api_lock = threading.Lock()

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.samba_key = os.environ.get("SAMBANOVA_API_KEY")
        
        # 2026 Stable Models
        self.primary_model = "llama-3.3-70b-versatile"
        self.backup_model = "Meta-Llama-3.3-70B-Instruct"
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        # We wrap the entire call in a lock to respect free-tier limits
        with api_lock:
            for attempt in range(3):  # Try 3 times total
                try:
                    # Attempt 1: Groq
                    if self.groq_client:
                        response = self.groq_client.chat.completions.create(
                            model=self.primary_model,
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=0.1
                        )
                        return schema.model_validate_json(response.choices[0].message.content)
                except Exception as e:
                    if "429" in str(e):
                        print(f"Groq Rate Limit hit. Cooling down for {5 + attempt * 2}s...")
                        time.sleep(5 + attempt * 2)  # Exponential wait
                    else:
                        print(f"Groq error: {str(e)}")
                
                # Attempt 2: SambaNova (Fallback within the same attempt)
                try:
                    if self.samba_client:
                        response = self.samba_client.chat.completions.create(
                            model=self.backup_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.1
                        )
                        return schema.model_validate_json(response.choices[0].message.content)
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(5)
                    else:
                        print(f"SambaNova error: {str(e)}")
            
            raise RuntimeError("All LLM providers are currently rate-limited. Please wait 60 seconds and try again.")
