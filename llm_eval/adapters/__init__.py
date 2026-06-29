from .base import BaseAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter
from .gemini_adapter import GeminiAdapter

ADAPTERS = {
    "gpt-4o": OpenAIAdapter,
    "gpt-4o-mini": OpenAIAdapter,
    "gpt-3.5-turbo": OpenAIAdapter,
    "claude-sonnet-4-6": AnthropicAdapter,
    "claude-haiku-4-5-20251001": AnthropicAdapter,
    "gemini-2.5-flash-preview-05-20": GeminiAdapter,
    "gemini-2.0-flash": GeminiAdapter,
    "gemini-1.5-flash": GeminiAdapter,
    "gemini-1.5-pro": GeminiAdapter,
}

def get_adapter(model: str, api_key: str = None) -> "BaseAdapter":
    if model not in ADAPTERS:
        raise ValueError(
            f"Unknown model '{model}'. Available: {list(ADAPTERS.keys())}"
        )
    return ADAPTERS[model](model=model, api_key=api_key)