# llm_eval/evaluators/registry.py
import importlib.util
import sys
from pathlib import Path
from .base import BaseEvaluator


class EvaluatorRegistry:
    """
    Allows users to register custom evaluators without modifying core code.
    Custom evaluators are Python files that define a class inheriting BaseEvaluator
    and expose it via an `EVALUATOR` variable.
    """
    _custom_evaluators = {}

    @classmethod
    def register(cls, name: str, evaluator_instance):
        cls._custom_evaluators[name] = evaluator_instance

    @classmethod
    def load_from_file(cls, name: str, file_path: str):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Custom evaluator file not found: {file_path}")

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "EVALUATOR"):
            raise ValueError(
                f"Custom evaluator file {file_path} must define an `EVALUATOR` instance"
            )

        cls.register(name, module.EVALUATOR)

    @classmethod
    def get(cls, name: str):
        return cls._custom_evaluators.get(name)

    @classmethod
    def all(cls):
        return cls._custom_evaluators