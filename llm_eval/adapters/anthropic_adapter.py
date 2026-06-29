import time
import anthropic
from .base import BaseAdapter


class AnthropicAdapter(BaseAdapter):
    def __init__(self, model: str = "claude-sonnet-4-6", api_key: str = None):
        super().__init__(model, api_key)
        self.client = anthropic.Anthropic(api_key=api_key)

    def complete(self, prompt: str, system_prompt: str = None) -> dict:
        kwargs = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        start = time.time()
        response = self.client.messages.create(**kwargs)
        latency = time.time() - start

        return {
            "text": response.content[0].text,
            "tokens": response.usage.input_tokens + response.usage.output_tokens,
            "latency": round(latency, 3),
        }