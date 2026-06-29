import pytest
from llm_eval.evaluators.rule_based import (
    ContainsEvaluator,
    NotContainsEvaluator,
    MaxWordsEvaluator,
    MinWordsEvaluator,
    RegexEvaluator,
    StartsWithEvaluator,
)


def test_contains_pass():
    ev = ContainsEvaluator()
    result = ev.evaluate("The capital of France is Paris", value="Paris")
    assert result["passed"] is True


def test_contains_fail():
    ev = ContainsEvaluator()
    result = ev.evaluate("The capital of France is Paris", value="London")
    assert result["passed"] is False


def test_not_contains_pass():
    ev = NotContainsEvaluator()
    result = ev.evaluate("The capital of France is Paris", value="London")
    assert result["passed"] is True


def test_not_contains_fail():
    ev = NotContainsEvaluator()
    result = ev.evaluate("I cannot help with that", value="cannot")
    assert result["passed"] is False


def test_max_words_pass():
    ev = MaxWordsEvaluator()
    result = ev.evaluate("This is a short sentence", value=10)
    assert result["passed"] is True


def test_max_words_fail():
    ev = MaxWordsEvaluator()
    result = ev.evaluate("one two three four five six seven eight nine ten eleven", value=5)
    assert result["passed"] is False


def test_min_words_pass():
    ev = MinWordsEvaluator()
    result = ev.evaluate("one two three four five", value=3)
    assert result["passed"] is True


def test_min_words_fail():
    ev = MinWordsEvaluator()
    result = ev.evaluate("too short", value=10)
    assert result["passed"] is False


def test_regex_pass():
    ev = RegexEvaluator()
    result = ev.evaluate("def reverse_string(s):", value=r"def \w+\(")
    assert result["passed"] is True


def test_regex_fail():
    ev = RegexEvaluator()
    result = ev.evaluate("no function here", value=r"def \w+\(")
    assert result["passed"] is False


def test_starts_with_pass():
    ev = StartsWithEvaluator()
    result = ev.evaluate("Paris is the capital", value="Paris")
    assert result["passed"] is True


def test_starts_with_fail():
    ev = StartsWithEvaluator()
    result = ev.evaluate("The capital is Paris", value="Paris")
    assert result["passed"] is False