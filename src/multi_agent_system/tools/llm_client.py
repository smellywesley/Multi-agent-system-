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
        
        # PROPER ROUTING: Give each API its exact correct model name
        self.groq_model = "llama-3.1-8b-instant" 
        self.samba_model = "Meta-Llama-3.3-70B-Instruct" 
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        if "json" not in prompt.lower():
            prompt += "\n\nYou MUST respond in strict JSON format."

        last_error = "Unknown Error"

        with api_lock:
            for attempt in range(3):
                try:
                    # --- Attempt 1: Groq ---
                    if self.groq_client:
                        response = self.groq_client.chat.completions.create(
                            model=self.groq_model, # Using Groq's exact name
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=0.1
                        )
                        content = response.choices[0].message.content
                        if content.startswith("```json"):
                            content = content.replace("```json", "").replace("```", "").strip()
                            
                        result = schema.model_validate_json(content)
                        time.sleep(3)
                        return result
                except Exception as e:
                    last_error = f"Groq Error: {str(e)}"
                    if "429" in str(e):
                        time.sleep(5)
                
                # --- Attempt 2: SambaNova Backup ---
                try:
                    if self.samba_client:
                        response = self.samba_client.chat.completions.create(
                            model=self.samba_model, # Using SambaNova's exact name
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
                        time.sleep(5)

            raise RuntimeError(f"SYSTEM HALTED. {last_error}")
