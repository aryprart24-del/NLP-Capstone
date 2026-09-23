"""
BhashaAI — Evaluation Dashboard Page
Run BLEU/chrF evaluations across language pairs, export CSV, generate graphs.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.config import (
    SUPPORTED_LANGUAGES, LANGUAGE_NAMES, DEFAULT_EVAL_PAIRS,
    EVALUATION_DIR, METRICS_DIR, GRAPHS_DIR,
)
from src.evaluator import (
    evaluate_language_pair, save_results_csv, generate_graphs, compute_bleu, compute_chrf,
)
from src.utils import format_time

st.set_page_config(page_title="BhashaAI — Evaluation", page_icon="📊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .eval-header {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="eval-header">📊 Evaluation Dashboard</h1>', unsafe_allow_html=True)
st.caption("Measure translation quality with BLEU and chrF metrics across language pairs")

# ── Tabs ───────────────────────────────────────────────────────
tab_single, tab_multi, tab_results = st.tabs(["Single Pair", "Multi-Pair Evaluation", "Saved Results"])

# ── Tab 1: Single Pair Evaluation ──────────────────────────────
with tab_single:
    st.markdown("### Evaluate a Single Language Pair")

    col1, col2 = st.columns(2)
    with col1:
        eval_src = st.selectbox("Source Language", LANGUAGE_NAMES, index=0, key="eval_src")
    with col2:
        eval_tgt = st.selectbox("Target Language", LANGUAGE_NAMES, index=1, key="eval_tgt")

    # Dataset source
    dataset_option = st.radio(
        "Dataset",
        ["Upload CSV", "Use built-in dataset"],
        key="eval_dataset_opt",
    )

    eval_df = None
    if dataset_option == "Upload CSV":
        uploaded = st.file_uploader(
            "Upload evaluation CSV (columns: source, reference)",
            type=["csv"],
            key="eval_csv_upload",
        )
        if uploaded:
            eval_df = pd.read_csv(uploaded)
            st.dataframe(eval_df.head(), use_container_width=True)
    else:
        src_code = eval_src[:2].lower()
        tgt_code = eval_tgt[:2].lower()
        builtin_path = EVALUATION_DIR / f"{src_code}_{tgt_code}.csv"
        if builtin_path.exists():
            eval_df = pd.read_csv(builtin_path)
            st.success(f"Loaded built-in dataset: {builtin_path.name} ({len(eval_df)} samples)")
            st.dataframe(eval_df.head(), use_container_width=True)
        else:
            st.warning(f"No built-in dataset found at `{builtin_path}`. Please upload one.")

    if st.button("▶️ Run Evaluation", type="primary", key="run_single_eval") and eval_df is not None:
        progress_bar = st.progress(0)
        status = st.empty()

        def update_progress(current, total):
            progress_bar.progress(current / total)
            status.text(f"Translating {current}/{total} samples...")

        with st.spinner("Running evaluation..."):
            result = evaluate_language_pair(
                eval_src, eval_tgt,
                dataset_df=eval_df,
                progress_callback=update_progress,
            )

        if result.get("error"):
            st.error(f"❌ {result['error']}")
        else:
            status.text("✅ Evaluation complete!")

            # Display metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("BLEU", f"{result['bleu']:.2f}")
            m2.metric("chrF", f"{result['chrf']:.2f}")
            m3.metric("Avg Time", format_time(result['avg_inference_time']))
            m4.metric("Samples", result['num_samples'])

            st.info(f"Total evaluation time: **{format_time(result['total_inference_time'])}**")

            # Detailed per-sample results
            with st.expander("Per-sample results"):
                detail_df = pd.DataFrame({
                    "Source": result["sources"],
                    "Reference": result["references"],
                    "Prediction": result["predictions"],
                    "Inference Time (s)": [f"{t:.4f}" for t in result["inference_times"]],
                })
                st.dataframe(detail_df, use_container_width=True)

            # Save
            if st.button("💾 Save Results to CSV", key="save_single"):
                path = save_results_csv([result], f"eval_{eval_src[:2].lower()}_{eval_tgt[:2].lower()}.csv")
                st.success(f"Saved to `{path}`")

# ── Tab 2: Multi-Pair Evaluation ───────────────────────────────
with tab_multi:
    st.markdown("### Evaluate Multiple Language Pairs")
    st.caption("Select pairs to evaluate. Each pair needs a corresponding dataset in `data/evaluation/`.")

    # Show available pairs
    selected_pairs = []
    for src, tgt in DEFAULT_EVAL_PAIRS:
        src_code = src[:2].lower()
        tgt_code = tgt[:2].lower()
        dataset_exists = (EVALUATION_DIR / f"{src_code}_{tgt_code}.csv").exists()
        icon = "✅" if dataset_exists else "❌"

        if st.checkbox(f"{icon} {src} → {tgt}", value=dataset_exists, key=f"pair_{src}_{tgt}"):
            selected_pairs.append((src, tgt))

    if st.button("▶️ Run All Selected Evaluations", type="primary", key="run_multi_eval") and selected_pairs:
        all_results = []
        overall_progress = st.progress(0)

        for idx, (src, tgt) in enumerate(selected_pairs):
            st.markdown(f"**Evaluating: {src} → {tgt}...**")
            src_code = src[:2].lower()
            tgt_code = tgt[:2].lower()
            dataset_path = EVALUATION_DIR / f"{src_code}_{tgt_code}.csv"

            result = evaluate_language_pair(src, tgt, dataset_path=dataset_path)
            all_results.append(result)
            overall_progress.progress((idx + 1) / len(selected_pairs))

        # Summary table
        st.markdown("### 📋 Evaluation Summary")
        summary_rows = []
        for r in all_results:
            if r.get("error"):
                summary_rows.append({"Pair": r.get("pair", "?"), "Error": r["error"]})
            else:
                summary_rows.append({
                    "Pair": r["pair"],
                    "BLEU": r["bleu"],
                    "chrF": r["chrf"],
                    "Avg Time (s)": r["avg_inference_time"],
                    "Samples": r["num_samples"],
                })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

        # Save & graph
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Save All Results CSV", key="save_multi"):
                path = save_results_csv(all_results)
                st.success(f"Saved to `{path}`")
        with col_b:
            if st.button("📈 Generate Graphs", key="gen_graphs"):
                graph_paths = generate_graphs(all_results)
                for gp in graph_paths:
                    st.image(str(gp), use_container_width=True)
                st.success(f"Graphs saved to `{GRAPHS_DIR}`")

# ── Tab 3: Saved Results ───────────────────────────────────────
with tab_results:
    st.markdown("### 📁 Saved Evaluation Results")

    # List CSV files
    csv_files = list(METRICS_DIR.glob("*.csv"))
    if csv_files:
        for f in csv_files:
            with st.expander(f.name):
                df = pd.read_csv(f)
                st.dataframe(df, use_container_width=True)
    else:
        st.info("No saved results yet. Run an evaluation first.")

    # List graphs
    st.markdown("### 📈 Saved Graphs")
    graph_files = list(GRAPHS_DIR.glob("*.png"))
    if graph_files:
        for gf in graph_files:
            st.image(str(gf), caption=gf.stem.replace("_", " ").title(), use_container_width=True)
    else:
        st.info("No graphs generated yet.")
