import time
from google import genai
from .base import BaseAdapter


class GeminiAdapter(BaseAdapter):
    def __init__(self, model: str = "gemini-1.5-flash", api_key: str = None):
        super().__init__(model, api_key)
        self.client = genai.Client(api_key=api_key)

    def complete(self, prompt: str, system_prompt: str = None) -> dict:
        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt

        start = time.time()
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config if config else None,
        )
        latency = time.time() - start

        return {
            "text": response.text,
            "tokens": response.usage_metadata.total_token_count,
            "latency": round(latency, 3),
        }