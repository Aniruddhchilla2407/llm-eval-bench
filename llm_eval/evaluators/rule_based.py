import re
from .base import BaseEvaluator


class ContainsEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: str, **kwargs) -> dict:
        passed = value.lower() in output.lower()
        return {
            "passed": passed,
            "reason": f"Expected to contain '{value}'" if not passed else f"Found '{value}'",
            "score": None,
        }


class NotContainsEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: str, **kwargs) -> dict:
        passed = value.lower() not in output.lower()
        return {
            "passed": passed,
            "reason": f"Expected NOT to contain '{value}'" if not passed else f"Did not find '{value}'",
            "score": None,
        }


class MaxWordsEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: int, **kwargs) -> dict:
        word_count = len(output.split())
        passed = word_count <= value
        return {
            "passed": passed,
            "reason": f"Word count: {word_count} {'<=' if passed else '>'} {value}",
            "score": None,
        }


class MinWordsEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: int, **kwargs) -> dict:
        word_count = len(output.split())
        passed = word_count >= value
        return {
            "passed": passed,
            "reason": f"Word count: {word_count} {'>=' if passed else '<'} {value}",
            "score": None,
        }


class RegexEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: str, **kwargs) -> dict:
        match = re.search(value, output)
        passed = match is not None
        return {
            "passed": passed,
            "reason": f"Regex '{value}' {'matched' if passed else 'did not match'}",
            "score": None,
        }


class StartsWithEvaluator(BaseEvaluator):
    def evaluate(self, output: str, value: str, **kwargs) -> dict:
        passed = output.strip().lower().startswith(value.lower())
        return {
            "passed": passed,
            "reason": f"Expected to start with '{value}'" if not passed else f"Starts with '{value}'",
            "score": None,
        }


RULE_EVALUATORS = {
    "contains": ContainsEvaluator(),
    "not_contains": NotContainsEvaluator(),
    "max_words": MaxWordsEvaluator(),
    "min_words": MinWordsEvaluator(),
    "regex": RegexEvaluator(),
    "starts_with": StartsWithEvaluator(),
}