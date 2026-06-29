import yaml
import json
from pathlib import Path


def load_suite(path: str) -> dict:
    """
    Load a test suite from a YAML or JSON file.
    Returns a normalized dict with suite metadata and tests.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Test suite file not found: {path}")

    with open(file_path, "r") as f:
        if file_path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(f)
        elif file_path.suffix == ".json":
            data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}. Use .yaml or .json")

    _validate_suite(data, path)
    return data


def _validate_suite(data: dict, path: str):
    if not isinstance(data, dict):
        raise ValueError(f"Invalid suite format in {path}: root must be a mapping")

    if "tests" not in data:
        raise ValueError(f"Suite {path} must have a 'tests' key")

    if not isinstance(data["tests"], list) or len(data["tests"]) == 0:
        raise ValueError(f"Suite {path} must have at least one test")

    for i, test in enumerate(data["tests"]):
        if "prompt" not in test:
            raise ValueError(f"Test #{i+1} in {path} is missing 'prompt'")
        if "expect" not in test:
            raise ValueError(f"Test #{i+1} in {path} is missing 'expect'")
        if not isinstance(test["expect"], list):
            raise ValueError(f"Test #{i+1} 'expect' must be a list of evaluators")