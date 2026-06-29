from .base import BaseEvaluator


JUDGE_PROMPT = """You are an impartial evaluator. You will be given:
- A prompt that was sent to an AI
- The AI's response
- A rubric to evaluate the response

Score the response from 1 to {out_of} based on the rubric.
Respond in this exact format:
SCORE: <number>
REASON: <one sentence explanation>

Rubric: {rubric}

Prompt: {prompt}

Response: {response}"""


class LLMJudgeEvaluator(BaseEvaluator):
    def __init__(self, adapter):
        self.adapter = adapter

    def evaluate(self, output: str, prompt: str, rubric: str,
                 score_threshold: float = 4, out_of: int = 5, **kwargs) -> dict:

        judge_prompt = JUDGE_PROMPT.format(
            out_of=out_of,
            rubric=rubric,
            prompt=prompt,
            response=output,
        )

        result = self.adapter.complete(judge_prompt)
        judge_output = result["text"]

        score = self._parse_score(judge_output)
        reason = self._parse_reason(judge_output)
        passed = score >= score_threshold if score is not None else False

        return {
            "passed": passed,
            "reason": f"Judge score: {score}/{out_of} — {reason}",
            "score": score,
        }

    def _parse_score(self, text: str):
        for line in text.splitlines():
            if line.startswith("SCORE:"):
                try:
                    return float(line.replace("SCORE:", "").strip())
                except ValueError:
                    return None
        return None

    def _parse_reason(self, text: str):
        for line in text.splitlines():
            if line.startswith("REASON:"):
                return line.replace("REASON:", "").strip()
        return "No reason provided"