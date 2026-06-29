from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Abstract base class for all LLM provider adapters.
    Every adapter must implement the `complete` method.
    """

    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.api_key = api_key

    @abstractmethod
    def complete(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Send a prompt to the LLM and return a normalized response.

        Returns:
            {
                "text": str,        # the model's response text
                "tokens": int,      # total tokens used
                "latency": float    # response time in seconds
            }
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(model={self.model})"