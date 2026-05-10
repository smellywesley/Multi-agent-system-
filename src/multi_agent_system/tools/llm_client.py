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
        
        self.groq_model = "llama-3.1-8b-instant" 
        self.samba_model = "Meta-Llama-3.3-70B-Instruct" 
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel], use_heavy_model: bool = False) -> Any:
        import json 
        
        schema_blueprint = json.dumps(schema.model_json_schema(), indent=2)
        
        prompt += "\n\n--- CRITICAL SYSTEM INSTRUCTION ---"
        prompt += "\nYou MUST respond in strict JSON format."
        prompt += f"\nYour JSON response MUST STRICTLY follow this exact JSON schema blueprint:\n{schema_blueprint}"

        error_log = []
        
        # THE DUAL-ENGINE SWITCH
        # If true, use the 70B Genius. If false, use the 8B Speedster.
        primary = "llama-3.3-70b-versatile" if use_heavy_model else self.groq_model
        backup = "Meta-Llama-3.3-70B-Instruct" if use_heavy_model else self.samba_model

        with api_lock:
            for attempt in range(3):
                # --- Attempt 1: Primary Engine ---
                if self.groq_client:
                    try:
                        response = self.groq_client.chat.completions.create(
                            model=primary,
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
                        error_log.append(f"Groq ({primary}): {str(e)}")
                        if "429" in str(e):
                            time.sleep(10)
                else:
                    error_log.append("Groq: Client missing API Key.")

                # --- Attempt 2: Backup Engine ---
                if self.samba_client:
                    try:
                        response = self.samba_client.chat.completions.create(
                            model=backup,
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
                        error_log.append(f"Samba ({backup}): {str(e)}")
                        if "429" in str(e):
                            time.sleep(10)
                else:
                    error_log.append("Samba: Client missing API Key.")

            final_errors = " | ".join(error_log[-2:]) 
            raise RuntimeError(f"DIAGNOSTIC HALT. Reasons -> {final_errors}")
