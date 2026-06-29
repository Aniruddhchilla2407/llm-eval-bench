from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators.
    Every evaluator takes the LLM output and returns a result dict.
    """

    @abstractmethod
    def evaluate(self, output: str, **kwargs) -> dict:
        """
        Evaluate the LLM output.

        Returns:
            {
                "passed": bool,
                "reason": str,
                "score": float | None
            }
        """
        pass