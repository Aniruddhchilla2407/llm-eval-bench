from .base import BaseEvaluator


class SemanticSimilarityEvaluator(BaseEvaluator):
    def __init__(self):
        self._model = None

    def _load_model(self):
        # lazy load so startup is fast when not using semantic eval
        if self._model is None:
            from sentence_transformers import SentenceTransformer, util
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._util = util

    def evaluate(self, output: str, expected: str, threshold: float = 0.75, **kwargs) -> dict:
        self._load_model()
        embeddings = self._model.encode([output, expected], convert_to_tensor=True)
        score = float(self._util.cos_sim(embeddings[0], embeddings[1]))
        passed = score >= threshold
        return {
            "passed": passed,
            "reason": f"Semantic similarity: {score:.2f} {'>=' if passed else '<'} {threshold}",
            "score": round(score, 3),
        }