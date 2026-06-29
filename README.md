# llm-eval-bench

A lightweight, local CLI tool for evaluating LLM prompt outputs against YAML-defined test suites.

No account. No cloud. No lock-in. Just `pip install` and a YAML file.

---

## Why

Most LLM evaluation tools are cloud-based, require accounts, and send your data to third-party servers. `llm-eval-bench` runs entirely on your machine — your prompts and outputs stay local.

---

## Features

- **Rule-based evaluators** — `contains`, `not_contains`, `max_words`, `min_words`, `regex`, `starts_with`
- **Semantic similarity** — embedding-based similarity scoring using `sentence-transformers`, runs fully locally
- **LLM-as-judge** — use any supported model to score outputs against a rubric
- **Model comparison** — run the same suite against two models and compare results side by side
- **Multiple providers** — OpenAI, Anthropic, Google Gemini
- **JSON output** — save results to a file for CI/CD pipelines

---

## Install

```bash
pip install llm-eval-bench
```

---

## Quick Start

**1. Create a test suite:**

```yaml
# my_suite.yaml
suite: "My Prompt Tests"
model: gpt-4o-mini

tests:
  - name: "Capital city"
    prompt: "What is the capital of France?"
    expect:
      - type: contains
        value: "Paris"
      - type: max_words
        value: 50

  - name: "Code generation"
    prompt: "Write a Python function to reverse a string. Return only the code."
    expect:
      - type: contains
        value: "def "
      - type: regex
        value: "def \\w+\\("

  - name: "Tone check"
    prompt: "Write a formal email declining a job offer"
    expect:
      - type: not_contains
        value: "hey"
      - type: llm_judge
        rubric: "Is this email professional and polite?"
        score_threshold: 4
        out_of: 5
```

**2. Run it:**

```bash
llm-eval run --suite my_suite.yaml --api-key YOUR_API_KEY
```

**3. See results:**

```
llm-eval-bench — My Prompt Tests
...
Results: 3/3 passed  |  Avg latency: 1.4s  |  Avg tokens: 54
```

## Supported Models

| Provider  | Models                                      |
|-----------|---------------------------------------------|
| OpenAI    | `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`  |
| Anthropic | `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` |
| Gemini    | `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro` |

---

## Evaluator Reference

### Rule-based

```yaml
expect:
  - type: contains
    value: "Paris"

  - type: not_contains
    value: "I cannot"

  - type: max_words
    value: 50

  - type: min_words
    value: 10

  - type: regex
    value: "def \\w+\\("

  - type: starts_with
    value: "The"
```

### Semantic Similarity

Runs locally using `sentence-transformers`. No API key needed.

```yaml
expect:
  - type: semantic_similarity
    expected: "Water boils at 100 degrees Celsius"
    threshold: 0.75  # 0.0 to 1.0, default 0.75
```

### LLM-as-Judge

```yaml
expect:
  - type: llm_judge
    rubric: "Is this explanation clear and accurate?"
    score_threshold: 4   # minimum passing score
    out_of: 5            # maximum score
```

---

## Commands

### Run a suite

```bash
llm-eval run --suite my_suite.yaml --api-key YOUR_KEY
```

Options:
- `--model` — override the model set in the YAML file
- `--judge-model` — use a different model as the LLM judge
- `--output results.json` — save results to a JSON file

### Compare two models

```bash
llm-eval compare \
  --suite my_suite.yaml \
  --baseline gpt-4o \
  --candidate gpt-4o-mini \
  --baseline-api-key YOUR_KEY \
  --candidate-api-key YOUR_KEY
```

### Save results to JSON

```bash
llm-eval run --suite my_suite.yaml --api-key YOUR_KEY --output results.json
```

---

## Environment Variables

Instead of passing `--api-key` every time, set environment variables:

```bash
export LLM_API_KEY=your-key-here
export JUDGE_API_KEY=your-judge-key-here  # optional, defaults to LLM_API_KEY
```

---

## Use in CI/CD

```yaml
# .github/workflows/eval.yml
- name: Run LLM eval
  run: |
    pip install llm-eval-bench
    llm-eval run --suite tests/prompts.yaml --output results.json
  env:
    LLM_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Project Structure

```
llm_eval/
├── cli.py           # entry point
├── runner.py        # orchestrates the full eval pipeline
├── loader.py        # parses YAML/JSON test suites
├── reporter.py      # terminal and JSON output
├── adapters/        # one file per LLM provider
└── evaluators/      # rule_based, semantic, llm_judge
```
## License

MIT — see [LICENSE](LICENSE)