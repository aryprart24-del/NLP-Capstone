"""
BhashaAI — Evaluation Engine
BLEU, chrF computation, multi-language pair evaluation, CSV export, and graphing.
"""

import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import pandas as pd
from evaluation.metrics import bleu as _bleu_func, chrf as _chrf_func

def compute_bleu(predictions: List[str], references: List[str]) -> float:
    """Compute corpus-level BLEU score.

    Returns:
        BLEU score (0-100 scale)
    """
    res = _bleu_func(predictions, references)
    return res["score"]


def compute_chrf(predictions: List[str], references: List[str]) -> float:
    """Compute corpus-level chrF score.

    Returns:
        chrF score (0-100 scale)
    """
    res = _chrf_func(predictions, references)
    return res["score"]


def evaluate_language_pair(
    source_lang: str,
    target_lang: str,
    dataset_path: Optional[Path] = None,
    dataset_df: Optional[pd.DataFrame] = None,
    progress_callback=None,
) -> Dict[str, Any]:
    """Run full evaluation on a language pair.

    Args:
        source_lang: Display name (e.g. "English")
        target_lang: Display name (e.g. "Hindi")
        dataset_path: Path to CSV with 'source' and 'reference' columns
        dataset_df: Alternative: pass a DataFrame directly
        progress_callback: Optional callable(current, total) for UI progress

    Returns:
        Dict with BLEU, chrF, timing, sample count, per-sample results
    """
    # Load model first
    load_model()

    # Load dataset
    if dataset_df is not None:
        df = dataset_df
    elif dataset_path is not None and dataset_path.exists():
        df = pd.read_csv(dataset_path)
    else:
        return {"error": f"No dataset found for {source_lang} → {target_lang}"}

    if "source" not in df.columns or "reference" not in df.columns:
        return {"error": "Dataset must have 'source' and 'reference' columns"}

    sources = df["source"].tolist()
    references = df["reference"].tolist()
    total = len(sources)

    if total == 0:
        return {"error": "Dataset is empty"}

    # Translate each source sentence
    predictions = []
    inference_times = []

    with timer() as total_timer:
        for i, src_text in enumerate(sources):
            result = translate_text(
                text=str(src_text),
                source_lang=source_lang,
                target_lang=target_lang,
            )
            predictions.append(result["translated_text"])
            inference_times.append(result["translation_time"])

            if progress_callback:
                progress_callback(i + 1, total)

    # Compute metrics
    bleu_score = compute_bleu(predictions, references)
    chrf_score = compute_chrf(predictions, references)
    avg_time = sum(inference_times) / len(inference_times) if inference_times else 0

    return {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "pair": f"{source_lang} → {target_lang}",
        "bleu": bleu_score,
        "chrf": chrf_score,
        "avg_inference_time": round(avg_time, 4),
        "total_inference_time": round(total_timer.elapsed, 2),
        "num_samples": total,
        "predictions": predictions,
        "references": references,
        "sources": sources,
        "inference_times": inference_times,
        "error": None,
    }


def run_multi_pair_evaluation(
    pairs: List[Tuple[str, str]],
    progress_callback=None,
) -> List[Dict[str, Any]]:
    """Evaluate multiple language pairs.

    Args:
        pairs: List of (source_lang, target_lang) tuples
        progress_callback: Optional callable(pair_name, pair_idx, total_pairs)

    Returns:
        List of evaluation result dicts
    """
    results = []
    for idx, (src, tgt) in enumerate(pairs):
        if progress_callback:
            progress_callback(f"{src} → {tgt}", idx, len(pairs))

        # Auto-find dataset
        src_code = src[:2].lower()
        tgt_code = tgt[:2].lower()
        dataset_path = EVALUATION_DIR / f"{src_code}_{tgt_code}.csv"

        result = evaluate_language_pair(src, tgt, dataset_path=dataset_path)
        results.append(result)

    return results


def save_results_csv(results: List[Dict[str, Any]], filename: str = "evaluation_results.csv") -> Path:
    """Save evaluation results to a CSV file.

    Returns:
        Path to saved CSV
    """
    rows = []
    for r in results:
        if r.get("error"):
            continue
        rows.append({
            "Language Pair": r["pair"],
            "BLEU": r["bleu"],
            "chrF": r["chrf"],
            "Avg Inference Time (s)": r["avg_inference_time"],
            "Total Time (s)": r["total_inference_time"],
            "Samples": r["num_samples"],
        })

    df = pd.DataFrame(rows)
    output_path = METRICS_DIR / filename
    df.to_csv(output_path, index=False)
    logger.info(f"Results saved to {output_path}")
    return output_path


def generate_graphs(results: List[Dict[str, Any]]) -> List[Path]:
    """Generate evaluation comparison graphs.

    Returns:
        List of paths to generated graph images
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns

    valid = [r for r in results if not r.get("error")]
    if not valid:
        return []

    sns.set_theme(style="darkgrid", palette="viridis")
    graph_paths = []

    # 1. BLEU & chrF comparison bar chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    pairs = [r["pair"] for r in valid]
    bleu_scores = [r["bleu"] for r in valid]
    chrf_scores = [r["chrf"] for r in valid]

    # BLEU
    bars1 = axes[0].barh(pairs, bleu_scores, color=sns.color_palette("viridis", len(pairs)))
    axes[0].set_xlabel("BLEU Score")
    axes[0].set_title("BLEU Scores by Language Pair", fontweight="bold")
    axes[0].set_xlim(0, max(bleu_scores) * 1.2 if bleu_scores else 100)
    for bar, score in zip(bars1, bleu_scores):
        axes[0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                     f"{score:.1f}", va="center", fontsize=9)

    # chrF
    bars2 = axes[1].barh(pairs, chrf_scores, color=sns.color_palette("magma", len(pairs)))
    axes[1].set_xlabel("chrF Score")
    axes[1].set_title("chrF Scores by Language Pair", fontweight="bold")
    axes[1].set_xlim(0, max(chrf_scores) * 1.2 if chrf_scores else 100)
    for bar, score in zip(bars2, chrf_scores):
        axes[1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                     f"{score:.1f}", va="center", fontsize=9)

    plt.tight_layout()
    path1 = GRAPHS_DIR / "bleu_chrf_comparison.png"
    fig.savefig(path1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    graph_paths.append(path1)

    # 2. Inference time comparison
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    avg_times = [r["avg_inference_time"] for r in valid]
    bars3 = ax2.bar(pairs, avg_times, color=sns.color_palette("coolwarm", len(pairs)))
    ax2.set_ylabel("Avg Inference Time (seconds)")
    ax2.set_title("Average Inference Time by Language Pair", fontweight="bold")
    ax2.set_xticklabels(pairs, rotation=45, ha="right")
    for bar, t in zip(bars3, avg_times):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{t:.3f}s", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    path2 = GRAPHS_DIR / "inference_time_comparison.png"
    fig2.savefig(path2, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    graph_paths.append(path2)

    logger.info(f"Generated {len(graph_paths)} graphs in {GRAPHS_DIR}")
    return graph_paths
