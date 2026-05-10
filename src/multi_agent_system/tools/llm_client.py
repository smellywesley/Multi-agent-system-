import os
import time
import threading
import json  # THE MISSING FIX
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
        
        # THE TYPE-AWARE ENFORCER: Detects Lists and builds the template
        fields = schema.model_fields
        template = {}
        has_list = False
        
        for key, field in fields.items():
            # Robust list detection
            is_list = "list" in str(field.annotation).lower()
            if is_list:
                template[key] = [f"<{field.description}>"]
                has_list = True
            else:
                template[key] = f"<{field.description}>"
        
        prompt += "\n\n--- REQUIRED OUTPUT FORMAT ---"
        prompt += "\nYou MUST respond in strict JSON format."
        prompt += f"\nYour JSON object MUST contain exactly these keys: {list(fields.keys())}"
        prompt += f"\nExample Structure:\n{json.dumps(template, indent=2)}"
        
        # DYNAMIC GUARDRAILS: Only give the AI rules that apply to its current task
        prompt += "\n\nCRITICAL INSTRUCTIONS:"
        prompt += "\n1. Do NOT include any technical schema definitions or 'properties'. Just the data."
        prompt += "\n2. Do NOT wrap plain string fields in arrays []."
        if has_list:
            prompt += "\n3. Fields shown as arrays [...] MUST be returned as JSON arrays, even if empty or containing only one item."

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
                            
                        parsed_json = json.loads(content)
                        if "properties" in parsed_json:
                            raise ValueError("AI returned schema instead of data.")
                            
                        result = schema.model_validate(parsed_json)
                        time.sleep(3)
                        return result
                    except Exception as e:
                        error_log.append(f"Groq ({primary}): {str(e)}")
                        time.sleep(5)

                if self.samba_client:
                    try:
                        response = self.samba_client.chat.completions.create(
                            model=backup,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.1
                        )
                        content = response.choices[0].message.content
                        parsed_json = json.loads(content)
                        result = schema.model_validate(parsed_json)
                        return result
                    except Exception as e:
                        error_log.append(f"Samba: {str(e)}")
                        time.sleep(5)

            raise RuntimeError(f"DIAGNOSTIC HALT. Reasons -> {' | '.join(error_log[-2:])}")
