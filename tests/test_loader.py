import pytest
import tempfile
import os
from llm_eval.loader import load_suite


VALID_YAML = """
suite: Test Suite
model: gpt-4o
tests:
  - name: Capital test
    prompt: What is the capital of France?
    expect:
      - type: contains
        value: Paris
"""

MISSING_TESTS_YAML = """
suite: Bad Suite
model: gpt-4o
"""

MISSING_PROMPT_YAML = """
suite: Bad Suite
tests:
  - name: No prompt
    expect:
      - type: contains
        value: Paris
"""

MISSING_EXPECT_YAML = """
suite: Bad Suite
tests:
  - name: No expect
    prompt: What is the capital of France?
"""


def write_temp_yaml(content):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_valid_suite_loads():
    path = write_temp_yaml(VALID_YAML)
    suite = load_suite(path)
    assert suite["suite"] == "Test Suite"
    assert len(suite["tests"]) == 1
    os.unlink(path)


def test_missing_tests_raises():
    path = write_temp_yaml(MISSING_TESTS_YAML)
    with pytest.raises(ValueError, match="tests"):
        load_suite(path)
    os.unlink(path)


def test_missing_prompt_raises():
    path = write_temp_yaml(MISSING_PROMPT_YAML)
    with pytest.raises(ValueError, match="prompt"):
        load_suite(path)
    os.unlink(path)


def test_missing_expect_raises():
    path = write_temp_yaml(MISSING_EXPECT_YAML)
    with pytest.raises(ValueError, match="expect"):
        load_suite(path)
    os.unlink(path)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_suite("nonexistent_file.yaml")