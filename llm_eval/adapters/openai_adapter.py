import time
import openai
from .base import BaseAdapter


class OpenAIAdapter(BaseAdapter):
    def __init__(self, model: str = "gpt-4o", api_key: str = None):
        super().__init__(model, api_key)
        self.client = openai.OpenAI(api_key=api_key)

    def complete(self, prompt: str, system_prompt: str = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        latency = time.time() - start

        return {
            "text": response.choices[0].message.content,
            "tokens": response.usage.total_tokens,
            "latency": round(latency, 3),
        }