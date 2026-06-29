from .loader import load_suite
from .adapters import get_adapter
from .evaluators import RULE_EVALUATORS, SemanticSimilarityEvaluator, LLMJudgeEvaluator


def run_suite(suite_path: str, model: str, api_key: str = None, judge_model: str = None, judge_api_key: str = None) -> dict:
    """
    Main orchestrator:
    1. Load suite
    2. Get adapter
    3. For each test: call LLM → run evaluators → collect results
    """
    suite = load_suite(suite_path)

    # model from CLI overrides model in yaml
    model = model or suite.get("model")
    if not model:
        raise ValueError("No model specified. Pass --model or set 'model' in your suite file.")

    adapter = get_adapter(model, api_key=api_key)

    # judge adapter — reuse main adapter if no separate judge model specified
    if judge_model:
        judge_adapter = get_adapter(judge_model, api_key=judge_api_key)
    else:
        judge_adapter = adapter

    semantic_evaluator = SemanticSimilarityEvaluator()
    judge_evaluator = LLMJudgeEvaluator(judge_adapter)

    results = []

    for test in suite["tests"]:
        name = test.get("name", test["prompt"][:50])
        prompt = test["prompt"]
        system_prompt = test.get("system_prompt", None)

        # call the LLM
        try:
            llm_result = adapter.complete(prompt, system_prompt=system_prompt)
            output = llm_result["text"]
            tokens = llm_result["tokens"]
            latency = llm_result["latency"]
            error = None
        except Exception as e:
            output = ""
            tokens = 0
            latency = 0
            error = str(e)

        # run each evaluator
        eval_results = []
        for expectation in test["expect"]:
            eval_type = expectation.get("type")

            try:
                if eval_type in RULE_EVALUATORS:
                    evaluator = RULE_EVALUATORS[eval_type]
                    result = evaluator.evaluate(output, **expectation)

                elif eval_type == "semantic_similarity":
                    result = semantic_evaluator.evaluate(
                        output,
                        expected=expectation["expected"],
                        threshold=expectation.get("threshold", 0.75),
                    )

                elif eval_type == "llm_judge":
                    result = judge_evaluator.evaluate(
                        output,
                        prompt=prompt,
                        rubric=expectation["rubric"],
                        score_threshold=expectation.get("score_threshold", 4),
                        out_of=expectation.get("out_of", 5),
                    )

                else:
                    result = {
                        "passed": False,
                        "reason": f"Unknown evaluator type: '{eval_type}'",
                        "score": None,
                    }

            except Exception as e:
                result = {
                    "passed": False,
                    "reason": f"Evaluator error: {str(e)}",
                    "score": None,
                }

            result["type"] = eval_type
            eval_results.append(result)

        overall_passed = all(r["passed"] for r in eval_results) and error is None

        results.append({
            "name": name,
            "prompt": prompt,
            "output": output,
            "tokens": tokens,
            "latency": latency,
            "error": error,
            "eval_results": eval_results,
            "passed": overall_passed,
        })

    return {
        "suite_name": suite.get("suite", suite_path),
        "model": model,
        "results": results,
    }


def compare_suites(suite_path: str, baseline_model: str, candidate_model: str,
                   baseline_api_key: str = None, candidate_api_key: str = None) -> dict:
    """
    Run the same suite against two models and return both results for comparison.
    """
    baseline = run_suite(suite_path, baseline_model, api_key=baseline_api_key)
    candidate = run_suite(suite_path, candidate_model, api_key=candidate_api_key)

    return {
        "suite_name": baseline["suite_name"],
        "baseline": baseline,
        "candidate": candidate,
    }