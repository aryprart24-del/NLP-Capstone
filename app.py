"""
BhashaAI — Multilingual Neural Machine Translation System
Main Streamlit Application Entry Point

Run with:  streamlit run app.py
"""

import streamlit as st

# ── Page Configuration (must be first Streamlit call) ──────────
st.set_page_config(
    page_title="BhashaAI — Multilingual Translation",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for premium look ────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }

    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-gpu {
        background: #065f46;
        color: #6ee7b7;
    }
    .status-cpu {
        background: #78350f;
        color: #fbbf24;
    }
    .status-loaded {
        background: #1e3a5f;
        color: #7dd3fc;
    }

    /* Card styling */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #818cf8;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Smooth transitions on buttons */
    .stButton > button {
        transition: all 0.2s ease;
        border-radius: 8px;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)


def main():
    # ── Sidebar: System Status ─────────────────────────────────
    with st.sidebar:
        st.markdown("## 🌐 BhashaAI")
        st.markdown("*Breaking Language Barriers with Multilingual AI*")
        st.divider()

        # Model loading status
        st.markdown("### ⚙️ System Status")

        # Check if model is loaded (import here to avoid circular)
        try:
            from src.translator import get_model_status
            status = get_model_status()

            if status["cuda_available"]:
                st.markdown(
                    '<span class="status-badge status-gpu">🟢 GPU Active</span>',
                    unsafe_allow_html=True,
                )
                st.caption(f"**GPU:** {status['gpu_name']}")
                st.caption(f"**VRAM:** {status['gpu_memory_total']}")
            else:
                st.markdown(
                    '<span class="status-badge status-cpu">🟡 CPU Mode</span>',
                    unsafe_allow_html=True,
                )

            st.caption(f"**PyTorch:** {status['torch_version']}")
            if status["cuda_version"]:
                st.caption(f"**CUDA:** {status['cuda_version']}")

            if status["model_loaded"]:
                st.markdown(
                    '<span class="status-badge status-loaded">✓ Model Loaded</span>',
                    unsafe_allow_html=True,
                )
                st.caption(f"**Load Time:** {status['model_load_time']}")
            else:
                st.info("Model will load on first translation.")

            st.caption(f"**Model:** NLLB-200-distilled-600M")

        except Exception as e:
            st.warning(f"Status unavailable: {e}")

        st.divider()

        # Supported languages
        st.markdown("### 🗣️ Supported Languages")
        from src.config import PRIMARY_LANGUAGES, SUPPORTED_LANGUAGES
        st.markdown("**Primary (Indian):**")
        for lang in PRIMARY_LANGUAGES:
            st.caption(f"• {lang}")
        st.markdown(f"**Total:** {len(SUPPORTED_LANGUAGES)} languages")

        st.divider()
        st.caption("B.Tech AI & Data Science Capstone")
        st.caption("© 2026 BhashaAI")

    # ── Main Content: Welcome ──────────────────────────────────
    st.markdown('<h1 class="main-header">🌐 BhashaAI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Multilingual Neural Machine Translation System — '
        'Breaking Language Barriers with AI</p>',
        unsafe_allow_html=True,
    )

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">15</div>
            <div class="metric-label">Languages</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">NLLB-200</div>
            <div class="metric-label">Model</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">GPU</div>
            <div class="metric-label">Accelerated</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">Local</div>
            <div class="metric-label">Privacy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature overview
    st.markdown("### 🚀 Features")
    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        st.markdown("#### 📝 Translation")
        st.markdown(
            "Translate text between **15 languages** including Hindi, Marathi, "
            "Bengali, Gujarati, and international languages. Auto-detect source language."
        )

    with feat_col2:
        st.markdown("#### 📄 Documents")
        st.markdown(
            "Upload **TXT, PDF, DOCX** files for full document translation. "
            "Long text is automatically segmented for optimal quality."
        )

    with feat_col3:
        st.markdown("#### 📊 Evaluation")
        st.markdown(
            "Measure translation quality with **BLEU and chrF** metrics. "
            "Compare language pairs and generate reports."
        )

    st.markdown("---")
    st.markdown(
        "👈 **Navigate using the sidebar** to access Translation, Document Translation, "
        "Evaluation, Error Analysis, Human Evaluation, and History pages."
    )


if __name__ == "__main__":
    main()
else:
    main()
