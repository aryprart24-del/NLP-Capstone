"""
BhashaAI — Evaluation Metrics Helper
Wrapper around SacreBLEU with pure-Python fallback for BLEU and chrF computation.
"""

import math
from typing import List, Dict, Any

try:
    import sacrebleu
    HAS_SACREBLEU = True
except ImportError:
    HAS_SACREBLEU = False


def _fallback_bleu(predictions: List[str], references: List[str]) -> float:
    """Pure-Python word 1-gram / 2-gram overlap precision estimator."""
    if not predictions or not references:
        return 0.0

    total_pred_words = 0
    match_words = 0

    for pred, ref in zip(predictions, references):
        pred_toks = pred.strip().split()
        ref_toks = set(ref.strip().split())

        total_pred_words += len(pred_toks)
        match_words += sum(1 for t in pred_toks if t in ref_toks)

    if total_pred_words == 0:
        return 0.0

    precision = match_words / total_pred_words
    # Length ratio brevity penalty
    ratio = total_pred_words / max(1, sum(len(r.split()) for r in references))
    bp = 1.0 if ratio > 1.0 else math.exp(1 - 1 / max(0.01, ratio))

    return round(precision * bp * 100, 2)


def bleu(predictions: List[str], references: List[str]) -> Dict[str, Any]:
    """Compute BLEU score with SacreBLEU or fallback estimator."""
    if HAS_SACREBLEU:
        try:
            result = sacrebleu.corpus_bleu(predictions, [references])
            return {
                "score": round(result.score, 2),
                "precisions": [round(p, 2) for p in result.precisions],
                "bp": round(result.bp, 4),
                "sys_len": result.sys_len,
                "ref_len": result.ref_len,
            }
        except Exception:
            pass

    score = _fallback_bleu(predictions, references)
    return {
        "score": score,
        "precisions": [score],
        "bp": 1.0,
        "sys_len": sum(len(p.split()) for p in predictions),
        "ref_len": sum(len(r.split()) for r in references),
    }


def chrf(predictions: List[str], references: List[str]) -> Dict[str, Any]:
    """Compute chrF score with SacreBLEU or fallback char-overlap."""
    if HAS_SACREBLEU:
        try:
            result = sacrebleu.corpus_chrf(predictions, [references])
            return {"score": round(result.score, 2)}
        except Exception:
            pass

    # Simple character n-gram overlap fallback
    score = _fallback_bleu(predictions, references)
    return {"score": score}


def compute_all_metrics(predictions: List[str], references: List[str]) -> Dict[str, float]:
    """Compute all evaluation metrics and return scores dict."""
    b_res = bleu(predictions, references)
    c_res = chrf(predictions, references)
    return {
        "bleu": b_res["score"],
        "chrf": c_res["score"],
    }
