"""
BhashaAI — Error Analysis Page
Structured framework for categorizing and recording translation errors.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.config import ERROR_CATEGORIES, ERROR_SEVERITY_LEVELS, ERROR_ANALYSIS_DIR

st.set_page_config(page_title="BhashaAI — Error Analysis", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .error-header {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="error-header">🔍 Error Analysis</h1>', unsafe_allow_html=True)
st.caption("Categorize and record translation errors across 10 linguistic categories")

ERROR_CSV = ERROR_ANALYSIS_DIR / "error_analysis.csv"

# ── Tabs ───────────────────────────────────────────────────────
tab_add, tab_view, tab_stats = st.tabs(["Add Error Record", "View Records", "Statistics"])

# ── Tab 1: Add Error ───────────────────────────────────────────
with tab_add:
    st.markdown("### Record a Translation Error")

    source_text = st.text_area("Source Text", height=80, key="err_source",
                               placeholder="The original source sentence")
    reference_text = st.text_area("Reference Translation", height=80, key="err_reference",
                                  placeholder="The correct human reference translation")
    prediction_text = st.text_area("Model Prediction", height=80, key="err_prediction",
                                   placeholder="What the model actually produced")

    col1, col2 = st.columns(2)
    with col1:
        error_category = st.selectbox("Error Category", ERROR_CATEGORIES, key="err_category")
    with col2:
        severity = st.selectbox("Severity", ERROR_SEVERITY_LEVELS, index=1, key="err_severity")

    explanation = st.text_area(
        "Explanation",
        height=100,
        key="err_explanation",
        placeholder="Explain why this is an error and what went wrong...",
    )

    if st.button("💾 Save Error Record", type="primary", key="save_error"):
        if not source_text.strip() or not prediction_text.strip():
            st.warning("Please fill in at least the Source Text and Model Prediction.")
        else:
            # Load or create CSV
            if ERROR_CSV.exists():
                df = pd.read_csv(ERROR_CSV)
            else:
                df = pd.DataFrame(columns=[
                    "source", "reference", "prediction",
                    "error_category", "explanation", "severity", "timestamp"
                ])

            new_row = pd.DataFrame([{
                "source": source_text.strip(),
                "reference": reference_text.strip(),
                "prediction": prediction_text.strip(),
                "error_category": error_category,
                "explanation": explanation.strip(),
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(ERROR_CSV, index=False)
            st.success(f"✅ Error record saved! ({len(df)} total records)")

    # Show category descriptions
    with st.expander("📖 Error Category Definitions"):
        categories_info = {
            "Morphological": "Errors in word forms, inflections, suffixes, or prefixes",
            "Syntactic": "Errors in sentence structure or grammatical arrangement",
            "Semantic": "Errors where the meaning is incorrectly conveyed",
            "Named Entity": "Errors in translating proper nouns, names, places",
            "Word Order": "Errors where words appear in unnatural order for the target language",
            "Omission": "Important words or phrases from the source are missing",
            "Addition": "Extra words or phrases not in the source are added",
            "Idiom": "Idiomatic expressions are translated literally instead of equivalently",
            "Long Context": "Errors caused by loss of context in long passages",
            "Code-Mixed": "Errors when input contains multiple languages (e.g., Hinglish)",
        }
        for cat, desc in categories_info.items():
            st.markdown(f"**{cat}:** {desc}")

# ── Tab 2: View Records ───────────────────────────────────────
with tab_view:
    st.markdown("### 📋 Error Analysis Records")

    if ERROR_CSV.exists():
        df = pd.read_csv(ERROR_CSV)
        if len(df) == 0:
            st.info("No error records yet.")
        else:
            # Filter
            filter_cat = st.multiselect("Filter by category", ERROR_CATEGORIES, key="err_filter_cat")
            if filter_cat:
                df = df[df["error_category"].isin(filter_cat)]

            st.dataframe(df, use_container_width=True)
            st.caption(f"Showing {len(df)} records")

            # Download
            csv_data = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv_data, "error_analysis.csv", "text/csv")
    else:
        st.info("No error records yet. Add some from the 'Add Error Record' tab.")

# ── Tab 3: Statistics ──────────────────────────────────────────
with tab_stats:
    st.markdown("### 📊 Error Analysis Statistics")

    if ERROR_CSV.exists():
        df = pd.read_csv(ERROR_CSV)
        if len(df) == 0:
            st.info("No data to analyze.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Errors by Category**")
                cat_counts = df["error_category"].value_counts()
                st.bar_chart(cat_counts)

            with col2:
                st.markdown("**Errors by Severity**")
                sev_counts = df["severity"].value_counts()
                st.bar_chart(sev_counts)

            st.metric("Total Error Records", len(df))
    else:
        st.info("No data to analyze yet.")
