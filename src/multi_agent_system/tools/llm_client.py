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
        # THE ZERO-META ENFORCER: A simpler approach for the 8B model
        # We list the keys and descriptions simply, without the technical 'JSON Schema' jargon
        fields = schema.model_fields
        template = {key: f"<{field.description}>" for key, field in fields.items()}
        
        prompt += "\n\n--- REQUIRED OUTPUT FORMAT ---"
        prompt += "\nYou MUST respond in strict JSON format."
        prompt += f"\nYour JSON object MUST contain exactly these keys: {list(fields.keys())}"
        prompt += f"\nExample Structure: {template}"
        prompt += "\nDo NOT include any technical schema definitions, 'properties', or 'types'. Just the data."

        error_log = []
        primary = "llama-3.3-70b-versatile" if use_heavy_model else self.groq_model
        backup = "Meta-Llama-3.3-70B-Instruct" if use_heavy_model else self.samba_model

        with api_lock:
            for attempt in range(3):
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
                            
                        # CRITICAL: If the AI STILL tries to return a 'properties' object, 
                        # we detect it here and force a retry.
                        parsed_json = json.loads(content)
                        if "properties" in parsed_json:
                            raise ValueError("AI returned schema instead of data.")
                            
                        result = schema.model_validate(parsed_json)
                        time.sleep(3)
                        return result
                    except Exception as e:
                        error_log.append(f"Groq ({primary}): {str(e)}")
                        time.sleep(5)
                
                # Backup logic (SambaNova) remains the same...
                # [KEEP YOUR EXISTING SAMBANOVA ATTEMPT BLOCK HERE]
                
            final_errors = " | ".join(error_log[-2:]) 
            raise RuntimeError(f"DIAGNOSTIC HALT. Reasons -> {final_errors}")
