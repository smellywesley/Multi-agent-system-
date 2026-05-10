import os
import time
import threading
from typing import Any, Type
from pydantic import BaseModel
import openai

api_lock = threading.Lock()

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.samba_key = os.environ.get("SAMBANOVA_API_KEY")
        
        # 8B handles the massive context, 70B is backup
        self.primary_model = "llama-3.1-8b-instant"
        self.backup_model = "llama-3.3-70b-versatile"
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        # 1. GROQ FIX: Force the word JSON into the prompt to prevent 400 API crashes
        if "json" not in prompt.lower():
            prompt += "\n\nYou MUST respond in strict JSON format."

        last_error = "Unknown Error"

        with api_lock:
            for attempt in range(3):  # 3 attempts is plenty if it's actually working
                try:
                    # --- Attempt 1: Groq ---
                    if self.groq_client:
                        response = self.groq_client.chat.completions.create(
                            model=self.primary_model,
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=0.1
                        )
                        # 2. MARKDOWN FIX: Strip markdown so Pydantic doesn't crash
                        content = response.choices[0].message.content
                        if content.startswith("```json"):
                            content = content.replace("```json", "").replace("```", "").strip()
                            
                        result = schema.model_validate_json(content)
                        time.sleep(3) # Gentle 3s cooldown
                        return result
                except Exception as e:
                    last_error = f"Groq Error: {str(e)}"
                    if "429" in str(e):
                        time.sleep(10)
                
                # --- Attempt 2: SambaNova Backup ---
                try:
                    if self.samba_client:
                        response = self.samba_client.chat.completions.create(
                            model=self.backup_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.1
                        )
                        content = response.choices[0].message.content
                        if content.startswith("```json"):
                            content = content.replace("```json", "").replace("```", "").strip()
                            
                        result = schema.model_validate_json(content)
                        time.sleep(3)
                        return result
                except Exception as e:
                    last_error = f"SambaNova Error: {str(e)}"
                    if "429" in str(e):
                        time.sleep(10)

            # 3. BRUTAL HONESTY: Output the ACTUAL error so we can see what broke
            raise RuntimeError(f"SYSTEM HALTED. {last_error}")
