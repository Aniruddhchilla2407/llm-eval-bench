from .loader import load_suite
from .adapters import get_adapter
from .evaluators import (
    RULE_EVALUATORS,
    SemanticSimilarityEvaluator,
    LLMJudgeEvaluator,
    EvaluatorRegistry,
)


def run_suite(
    suite_path: str,
    model: str,
    api_key: str = None,
    judge_model: str = None,
    judge_api_key: str = None,
) -> dict:
    suite = load_suite(suite_path)

    model = model or suite.get("model")
    if not model:
        raise ValueError(
            "No model specified. Pass --model or set 'model' in your suite file."
        )

    adapter = get_adapter(model, api_key=api_key)

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

                elif eval_type == "custom":
                    # load and run custom evaluator from user-provided file
                    custom_path = expectation.get("custom_evaluator_path")
                    custom_name = expectation.get("custom_evaluator_name", "custom")

                    if not custom_path:
                        raise ValueError(
                            "Custom evaluator requires 'custom_evaluator_path' in expect block"
                        )

                    # load from file if not already registered
                    if not EvaluatorRegistry.get(custom_name):
                        EvaluatorRegistry.load_from_file(custom_name, custom_path)

                    evaluator = EvaluatorRegistry.get(custom_name)
                    result = evaluator.evaluate(output, **expectation)

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


def compare_suites(
    suite_path: str,
    baseline_model: str,
    candidate_model: str,
    baseline_api_key: str = None,
    candidate_api_key: str = None,
) -> dict:
    baseline = run_suite(suite_path, baseline_model, api_key=baseline_api_key)
    candidate = run_suite(suite_path, candidate_model, api_key=candidate_api_key)

    return {
        "suite_name": baseline["suite_name"],
        "baseline": baseline,
        "candidate": candidate,
    }