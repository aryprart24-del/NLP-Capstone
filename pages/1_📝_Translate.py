"""
BhashaAI — Fast Interactive Translation Page
Supports Online Zero-Download Instant Mode and Local Offline NLLB-200 Mode.
"""

import streamlit as st
from src.config import SUPPORTED_LANGUAGES, LANGUAGE_NAMES, ENGINE_OPTIONS, ENGINE_ONLINE
from src.translator import translate_text, load_model
from src.history import save_translation
from src.utils import format_time, format_number

st.set_page_config(page_title="BhashaAI — Translate", page_icon="📝", layout="wide")

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .translate-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    .result-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        min-height: 140px;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #f8fafc;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stat-chip {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.8rem;
        color: #94a3b8;
    }
    .stat-value { color: #818cf8; font-weight: 600; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="translate-header">📝 Translate</h1>', unsafe_allow_html=True)
st.caption("Multilingual NMT — Instant Online Mode (0 MB Download) & Offline Local NLLB Mode")

# ── Engine Selection ──────────────────────────────────────────
selected_engine = st.radio(
    "Translation Engine",
    ENGINE_OPTIONS,
    index=0,
    horizontal=True,
    help="Online mode runs instantly with 0 MB download! Local mode uses offline NLLB-200 model.",
)

# ── Language Selection Row ─────────────────────────────────────
source_options = ["Auto Detect"] + LANGUAGE_NAMES
target_options = LANGUAGE_NAMES.copy()

if "src_lang_idx" not in st.session_state:
    st.session_state.src_lang_idx = 0  # Auto Detect
if "tgt_lang_idx" not in st.session_state:
    st.session_state.tgt_lang_idx = 1  # Hindi

col_src, col_swap, col_tgt = st.columns([5, 1, 5])

with col_src:
    source_lang = st.selectbox(
        "Source Language",
        source_options,
        index=st.session_state.src_lang_idx,
        key="source_lang_select",
    )

with col_swap:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⇄ Swap", use_container_width=True, key="swap_btn"):
        if source_lang != "Auto Detect":
            old_src = source_lang
            old_tgt = target_options[st.session_state.tgt_lang_idx]
            if old_tgt in source_options:
                st.session_state.src_lang_idx = source_options.index(old_tgt)
            if old_src in target_options:
                st.session_state.tgt_lang_idx = target_options.index(old_src)
            if "last_translation" in st.session_state and st.session_state.last_translation:
                st.session_state.input_text = st.session_state.last_translation
            st.rerun()
        else:
            st.warning("Select explicit source language to swap")

with col_tgt:
    target_lang = st.selectbox(
        "Target Language",
        target_options,
        index=st.session_state.tgt_lang_idx,
        key="target_lang_select",
    )

# ── Fast Form for Zero-Lag Text Input ──────────────────────────
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

with st.form("translation_form", clear_on_submit=False):
    input_text = st.text_area(
        "Enter text to translate",
        value=st.session_state.input_text,
        height=160,
        placeholder="Type or paste text here...\n\nExample: India is a country full of diversity.",
    )

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        translate_submitted = st.form_submit_button(
            "⚡ Translate Now", type="primary", use_container_width=True
        )
    with btn_col2:
        clear_submitted = st.form_submit_button(
            "🗑️ Clear Text", use_container_width=True
        )

if clear_submitted:
    st.session_state.input_text = ""
    if "last_translation" in st.session_state:
        del st.session_state.last_translation
    if "last_result" in st.session_state:
        del st.session_state.last_result
    st.rerun()

# ── Execute Translation ───────────────────────────────────────
if translate_submitted:
    st.session_state.input_text = input_text
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to translate.")
    else:
        auto = source_lang == "Auto Detect"
        with st.spinner("Translating..."):
            result = translate_text(
                text=input_text,
                source_lang=source_lang,
                target_lang=target_lang,
                auto_detect=auto,
                engine=selected_engine,
            )

        if result.get("error"):
            st.error(f"❌ {result['error']}")
        else:
            st.session_state.last_translation = result["translated_text"]
            st.session_state.last_result = result

            # Save translation history
            save_translation(
                source_text=result["source_text"],
                translated_text=result["translated_text"],
                source_lang=result["source_lang"],
                target_lang=result["target_lang"],
                translation_time=result["translation_time"],
                detected_lang=result.get("detected_lang"),
            )

# ── Display Translation Result ─────────────────────────────────
if "last_result" in st.session_state:
    result = st.session_state.last_result
    st.markdown("---")

    src_display = result["source_lang"]
    tgt_display = result["target_lang"]
    if result.get("detected_lang"):
        src_display = f"{result['detected_lang']} (auto-detected)"

    engine_tag = result.get("engine_used", "Online")
    st.markdown(f"### **{src_display}** ➔ **{tgt_display}**  *(via {engine_tag})*")

    # Output Card
    st.markdown(
        f'<div class="result-box">{result["translated_text"]}</div>',
        unsafe_allow_html=True,
    )

    # Performance Stats
    stats_html = (
        f'<span class="stat-chip">⚡ Latency: <span class="stat-value">{format_time(result["translation_time"])}</span></span>'
        f'<span class="stat-chip">Words: <span class="stat-value">'
        f'{format_number(result["word_count_source"])} → {format_number(result["word_count_target"])}'
        f'</span></span>'
        f'<span class="stat-chip">Chars: <span class="stat-value">'
        f'{format_number(result["char_count_source"])} → {format_number(result["char_count_target"])}'
        f'</span></span>'
        f'<span class="stat-chip">Engine: <span class="stat-value">{engine_tag}</span></span>'
    )
    st.markdown(stats_html, unsafe_allow_html=True)

    # Actions: Download & Quick Copy
    act_col1, act_col2, _ = st.columns([1, 1, 3])
    with act_col1:
        st.download_button(
            "📥 Download (.txt)",
            data=result["translated_text"],
            file_name=f"translation_{tgt_display.lower()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with act_col2:
        if st.button("📋 Copy Text", use_container_width=True):
            st.code(result["translated_text"], language=None)
            st.success("Copied to display box above!")
