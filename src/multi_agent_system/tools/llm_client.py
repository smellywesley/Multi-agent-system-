import os
import time
import threading
from typing import Any, Type
from pydantic import BaseModel
import openai

# Global lock to force agents into a single-file line
api_lock = threading.Lock()

class LLMClient:
    def __init__(self, settings=None, **kwargs):
        self.groq_key = os.environ.get("GROQ_API_KEY")
        self.samba_key = os.environ.get("SAMBANOVA_API_KEY")
        
       # BULLETPROOF FREE-TIER STACK
        # Using 8B for massive token limits (fixes TPM crashes)
        self.primary_model = "llama-3.1-8b-instant" 
        # Using 70B only as a backup for complex reasoning
        self.backup_model = "llama-3.3-70b-versatile"
        
        self.groq_client = openai.OpenAI(api_key=self.groq_key, base_url="https://api.groq.com/openai/v1") if self.groq_key else None
        self.samba_client = openai.OpenAI(api_key=self.samba_key, base_url="https://api.sambanova.ai/v1") if self.samba_key else None

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> Any:
        with api_lock:
            # Increased to 6 attempts to survive the 'cancer' query volume
            for attempt in range(6):  
                try:
                    # Attempt 1: Groq (Primary)
                    if self.groq_client:
                        response = self.groq_client.chat.completions.create(
                            model=self.primary_model,
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=0.1
                        )
                        result = schema.model_validate_json(response.choices[0].message.content)
                        # CRITICAL: 6-second cooldown after every successful extraction
                        # This keeps us under the 10 Requests Per Minute (RPM) limit
                        time.sleep(6) 
                        return result
                except Exception as e:
                    if "429" in str(e):
                        wait_time = 10 + (attempt * 5)
                        print(f"Rate Limit! Cooling down for {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"Groq Error: {str(e)}")

                # Attempt 2: SambaNova (Backup)
                try:
                    if self.samba_client:
                        response = self.samba_client.chat.completions.create(
                            model=self.backup_model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.1
                        )
                        result = schema.model_validate_json(response.choices[0].message.content)
                        time.sleep(6)
                        return result
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(10)
                    else:
                        print(f"SambaNova Error: {str(e)}")
            
            raise RuntimeError("CORE ERROR: Rate limits exceeded on all AI providers. The current query triggered a burst limit on the free tier. Please wait 60 seconds.")
