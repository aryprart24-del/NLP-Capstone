"""
BhashaAI — Standalone Batch Evaluation Script
Run from command line:  python evaluation/evaluate.py --pairs en_hi en_mr --dataset-dir data/evaluation/

This script can be run independently of Streamlit.
"""

import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from src.config import EVALUATION_DIR, SUPPORTED_LANGUAGES
from src.evaluator import evaluate_language_pair, save_results_csv, generate_graphs


# Map short codes to display names
CODE_TO_NAME = {
    "en": "English", "hi": "Hindi", "mr": "Marathi", "bn": "Bengali",
    "gu": "Gujarati", "fr": "French", "de": "German", "es": "Spanish",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ar": "Arabic",
    "zh": "Chinese", "ja": "Japanese", "ko": "Korean",
}


def main():
    parser = argparse.ArgumentParser(description="BhashaAI Batch Evaluation")
    parser.add_argument(
        "--pairs", nargs="+", required=True,
        help="Language pairs to evaluate (e.g., en_hi en_mr hi_en)"
    )
    parser.add_argument(
        "--dataset-dir", type=str, default=str(EVALUATION_DIR),
        help="Directory containing evaluation CSVs"
    )
    parser.add_argument(
        "--output", type=str, default="evaluation_results.csv",
        help="Output CSV filename"
    )
    parser.add_argument(
        "--graphs", action="store_true",
        help="Generate comparison graphs"
    )

    args = parser.parse_args()
    dataset_dir = Path(args.dataset_dir)

    all_results = []
    for pair_str in args.pairs:
        parts = pair_str.split("_")
        if len(parts) != 2:
            print(f"Invalid pair format: {pair_str} (expected: xx_yy)")
            continue

        src_code, tgt_code = parts
        src_name = CODE_TO_NAME.get(src_code, src_code)
        tgt_name = CODE_TO_NAME.get(tgt_code, tgt_code)

        dataset_path = dataset_dir / f"{src_code}_{tgt_code}.csv"
        if not dataset_path.exists():
            print(f"⚠️  Dataset not found: {dataset_path}")
            continue

        print(f"\n{'='*50}")
        print(f"Evaluating: {src_name} → {tgt_name}")
        print(f"Dataset: {dataset_path}")
        print(f"{'='*50}")

        result = evaluate_language_pair(src_name, tgt_name, dataset_path=dataset_path)

        if result.get("error"):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"  BLEU:           {result['bleu']:.2f}")
            print(f"  chrF:           {result['chrf']:.2f}")
            print(f"  Avg Time:       {result['avg_inference_time']:.4f}s")
            print(f"  Total Time:     {result['total_inference_time']:.2f}s")
            print(f"  Samples:        {result['num_samples']}")
            all_results.append(result)

    if all_results:
        path = save_results_csv(all_results, args.output)
        print(f"\n✅ Results saved to: {path}")

        if args.graphs:
            graph_paths = generate_graphs(all_results)
            for gp in graph_paths:
                print(f"📈 Graph saved: {gp}")


if __name__ == "__main__":
    main()
