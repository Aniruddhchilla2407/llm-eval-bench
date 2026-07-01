from llm_eval.evaluators.base import BaseEvaluator


class ProfessionalToneEvaluator(BaseEvaluator):
    """
    Example custom evaluator — checks that the output does not contain
    informal language. Users can write evaluators like this and plug them
    in without modifying llm-eval-bench's core code.
    """

    INFORMAL_WORDS = [
        "hey", "yeah", "nope", "gonna", "wanna",
        "gotta", "kinda", "sorta", "dunno", "yep",
    ]

    def evaluate(self, output: str, **kwargs) -> dict:
        found = [w for w in self.INFORMAL_WORDS if w in output.lower().split()]
        passed = len(found) == 0
        return {
            "passed": passed,
            "reason": (
                f"Informal words found: {found}" if not passed
                else "No informal language detected"
            ),
            "score": None,
        }


# This line is required — the registry looks for EVALUATOR at module level
EVALUATOR = ProfessionalToneEvaluator()