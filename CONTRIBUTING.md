# Contributing

## Setup
```bash
git clone https://github.com/Aniruddhchilla2407/llm-eval-bench
cd llm-eval-bench
pip install -e ".[dev]"
```

## Running Tests
```bash
python -m pytest tests/ -v
```

## Opening a PR
- Fork the repo
- Create a branch: `git checkout -b fix/your-fix-name`
- Make your changes
- Run tests to make sure nothing breaks
- Open a pull request with a clear description