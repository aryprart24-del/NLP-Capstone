"""
BhashaAI — Human Evaluation Page
Template and interface for human evaluators to rate translations.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.config import HUMAN_EVAL_CRITERIA, HUMAN_EVAL_DIR

st.set_page_config(page_title="BhashaAI — Human Evaluation", page_icon="👤", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .human-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="human-header">👤 Human Evaluation</h1>', unsafe_allow_html=True)
st.caption("Rate translation quality on Fluency, Adequacy, Meaning Preservation, and Grammar (1–5)")

HUMAN_CSV = HUMAN_EVAL_DIR / "human_evaluation.csv"

tab_eval, tab_view, tab_stats = st.tabs(["Evaluate", "View Evaluations", "Statistics"])

# ── Tab 1: Evaluate ───────────────────────────────────────────
with tab_eval:
    st.markdown("### Rate a Translation")

    evaluator_name = st.text_input("Evaluator Name", key="he_evaluator",
                                   placeholder="Your name")

    source_text = st.text_area("Source Text", height=80, key="he_source",
                               placeholder="The original source sentence")
    reference_text = st.text_area("Reference Translation", height=80, key="he_reference",
                                  placeholder="The correct human reference translation")
    prediction_text = st.text_area("Model Prediction", height=80, key="he_prediction",
                                   placeholder="What the model produced")

    st.markdown("### 📊 Ratings (1 = Poor, 5 = Excellent)")

    ratings = {}
    for criterion in HUMAN_EVAL_CRITERIA:
        name = criterion["name"]
        desc = criterion["description"]
        ratings[name.lower().replace(" ", "_")] = st.slider(
            f"**{name}** — {desc}",
            min_value=1, max_value=5, value=3,
            key=f"he_rating_{name}",
        )

    if st.button("💾 Save Evaluation", type="primary", key="save_human_eval"):
        if not evaluator_name.strip():
            st.warning("Please enter your name.")
        elif not source_text.strip() or not prediction_text.strip():
            st.warning("Please fill in at least Source Text and Model Prediction.")
        else:
            # Load or create CSV
            if HUMAN_CSV.exists():
                df = pd.read_csv(HUMAN_CSV)
            else:
                df = pd.DataFrame(columns=[
                    "source", "reference", "prediction",
                    "fluency", "adequacy", "meaning_preservation", "grammar",
                    "evaluator", "timestamp"
                ])

            new_row = pd.DataFrame([{
                "source": source_text.strip(),
                "reference": reference_text.strip(),
                "prediction": prediction_text.strip(),
                "fluency": ratings.get("fluency", 3),
                "adequacy": ratings.get("adequacy", 3),
                "meaning_preservation": ratings.get("meaning_preservation", 3),
                "grammar": ratings.get("grammar", 3),
                "evaluator": evaluator_name.strip(),
                "timestamp": datetime.now().isoformat(),
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(HUMAN_CSV, index=False)
            st.success(f"✅ Evaluation saved! ({len(df)} total evaluations)")

# ── Tab 2: View ───────────────────────────────────────────────
with tab_view:
    st.markdown("### 📋 Human Evaluation Records")

    if HUMAN_CSV.exists():
        df = pd.read_csv(HUMAN_CSV)
        if len(df) == 0:
            st.info("No evaluations yet.")
        else:
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total: {len(df)} evaluations")

            csv_data = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv_data, "human_evaluation.csv", "text/csv")
    else:
        st.info("No evaluations yet. Add some from the 'Evaluate' tab.")

# ── Tab 3: Statistics ──────────────────────────────────────────
with tab_stats:
    st.markdown("### 📊 Human Evaluation Statistics")

    if HUMAN_CSV.exists():
        df = pd.read_csv(HUMAN_CSV)
        if len(df) == 0:
            st.info("No data to analyze.")
        else:
            criteria_cols = ["fluency", "adequacy", "meaning_preservation", "grammar"]

            # Average scores
            st.markdown("**Average Scores Across All Evaluations**")
            avg_cols = st.columns(4)
            for i, col_name in enumerate(criteria_cols):
                if col_name in df.columns:
                    avg = df[col_name].mean()
                    display_name = col_name.replace("_", " ").title()
                    avg_cols[i].metric(display_name, f"{avg:.2f} / 5")

            st.metric("Total Evaluations", len(df))
            st.metric("Evaluators", df["evaluator"].nunique() if "evaluator" in df.columns else 0)

            # Score distribution
            st.markdown("**Score Distributions**")
            for col_name in criteria_cols:
                if col_name in df.columns:
                    st.markdown(f"**{col_name.replace('_', ' ').title()}**")
                    st.bar_chart(df[col_name].value_counts().sort_index())
    else:
        st.info("No data to analyze yet.")
