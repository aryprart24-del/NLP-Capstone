"""
BhashaAI — Translation History Page
View, search, and manage recent translations.
"""

import streamlit as st
from src.history import load_history, clear_history, get_recent

st.set_page_config(page_title="BhashaAI — History", page_icon="📜", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .history-header {
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    .history-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .history-lang {
        color: #818cf8;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .history-time {
        color: #64748b;
        font-size: 0.75rem;
    }
    .history-text {
        color: #e2e8f0;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="history-header">📜 Translation History</h1>', unsafe_allow_html=True)
st.caption("View your recent translations")

# ── Controls ───────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search_query = st.text_input("🔍 Search history", placeholder="Filter by text...", key="history_search")
with col2:
    max_items = st.selectbox("Show", [10, 20, 50, 100], index=1, key="history_count")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All History", key="clear_history_btn"):
        clear_history()
        st.success("History cleared!")
        st.rerun()

# ── Load and Display ───────────────────────────────────────────
history = get_recent(max_items)

if not history:
    st.info("No translations yet. Go to the **📝 Translate** page to start translating!")
else:
    # Filter by search
    if search_query:
        history = [
            h for h in history
            if search_query.lower() in h.get("source_text", "").lower()
            or search_query.lower() in h.get("translated_text", "").lower()
        ]

    st.markdown(f"**Showing {len(history)} translations**")

    for item in history:
        src = item.get("source_lang", "?")
        tgt = item.get("target_lang", "?")
        timestamp = item.get("timestamp", "")
        src_text = item.get("source_text", "")
        tgt_text = item.get("translated_text", "")
        t_time = item.get("translation_time", 0)

        # Truncate long texts for display
        src_preview = src_text[:200] + "..." if len(src_text) > 200 else src_text
        tgt_preview = tgt_text[:200] + "..." if len(tgt_text) > 200 else tgt_text

        st.markdown(f"""
        <div class="history-card">
            <div class="history-lang">{src} → {tgt}</div>
            <div class="history-time">{timestamp} • {t_time:.2f}s</div>
            <div class="history-text"><b>Source:</b> {src_preview}</div>
            <div class="history-text"><b>Translation:</b> {tgt_preview}</div>
        </div>
        """, unsafe_allow_html=True)
