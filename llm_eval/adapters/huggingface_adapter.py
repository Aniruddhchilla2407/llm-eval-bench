import time
from huggingface_hub import InferenceClient
from .base import BaseAdapter

class HuggingFaceAdapter(BaseAdapter):
    def __init__(self, model: str = "meta-llama/Llama-3.1-8B-Instruct", api_key: str = None):
        super().__init__(model, api_key)
        self.client = InferenceClient(token=api_key)

    def complete(self, prompt: str, system_prompt: str = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        response = self.client.chat_completion(
            messages=messages,
            model=self.model,
            max_tokens=512,
        )
        latency = time.time() - start

        return {
            "text": response.choices[0].message.content,
            "tokens": response.usage.total_tokens if response.usage else 0,
            "latency": round(latency, 3),
        }