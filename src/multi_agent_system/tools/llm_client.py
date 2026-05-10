import os
import time
import threading
import json
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
        
        # THE RECURSIVE BLUEPRINT BUILDER: Maps perfectly nested folders
        def build_template(model_class):
            temp = {}
            for k, f in model_class.model_fields.items():
                anno = f.annotation
                anno_str = str(anno).lower()
                
                is_list = "list" in anno_str
                
                # Dynamically look for nested Pydantic models
                inner_model = None
                if hasattr(anno, "__args__"):
                    for arg in anno.__args__:
                        if hasattr(arg, "model_fields"):
                            inner_model = arg
                            break
                elif hasattr(anno, "model_fields"):
                    inner_model = anno

                # Build the nested structure
                if is_list:
                    if inner_model:
                        temp[k] = [build_template(inner_model)]
                    else:
                        temp[k] = [f"<{f.description}>"]
                else:
                    if inner_model:
                        temp[k] = build_template(inner_model)
                    else:
                        temp[k] = f"<{f.description}>"
            return temp

        template = build_template(schema)
        
        prompt += "\n\n--- REQUIRED OUTPUT FORMAT ---"
        prompt += "\nYou MUST respond in strict JSON format."
        prompt += f"\nYour JSON object MUST contain exactly these root keys: {list(schema.model_fields.keys())}"
        prompt += f"\nExample Structure:\n{json.dumps(template, indent=2)}"
        
        prompt += "\n\nCRITICAL INSTRUCTIONS:"
        prompt += "\n1. Do NOT include any technical schema definitions or 'properties'. Just the data."
        prompt += "\n2. Do NOT wrap plain string fields in arrays []."
        prompt += "\n3. Maintain the EXACT nested structure shown in the Example Structure. Do not flatten the data."

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
