"""
BhashaAI — Document Translation Page
Upload TXT/PDF/DOCX files and translate their content.
"""

import streamlit as st
from src.config import SUPPORTED_LANGUAGES, LANGUAGE_NAMES
from src.document_processor import extract_text
from src.translator import translate_text, load_model
from src.text_processor import segment_sentences
from src.utils import format_time, format_number

st.set_page_config(page_title="BhashaAI — Documents", page_icon="📄", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .doc-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="doc-header">📄 Document Translation</h1>', unsafe_allow_html=True)
st.caption("Upload TXT, PDF, or DOCX files for full document translation")

# ── Language Selection ─────────────────────────────────────────
col_src, col_tgt = st.columns(2)
with col_src:
    source_lang = st.selectbox(
        "Source Language",
        ["Auto Detect"] + LANGUAGE_NAMES,
        index=0,
        key="doc_src_lang",
    )
with col_tgt:
    target_lang = st.selectbox(
        "Target Language",
        LANGUAGE_NAMES,
        index=1,  # Hindi
        key="doc_tgt_lang",
    )

# ── File Upload ────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "docx"],
    help="Supported formats: TXT, PDF, DOCX",
    key="doc_upload",
)

if uploaded_file is not None:
    # Extract text
    with st.spinner("Extracting text from document..."):
        file_content = uploaded_file.read()
        extracted_text = extract_text(file_content, uploaded_file.name)

    st.markdown("### 📖 Extracted Text")
    st.info(f"**File:** {uploaded_file.name} | **Characters:** {format_number(len(extracted_text))} | "
            f"**Words:** {format_number(len(extracted_text.split()))}")

    with st.expander("View extracted text", expanded=False):
        st.text(extracted_text[:5000] + ("..." if len(extracted_text) > 5000 else ""))

    # Translate button
    if st.button("🔄 Translate Document", type="primary", use_container_width=True, key="doc_translate_btn"):
        auto = source_lang == "Auto Detect"

        # Segment the document
        segments = segment_sentences(extracted_text)
        total = len(segments)

        st.markdown(f"**Translating {total} segments...**")
        progress_bar = st.progress(0)
        status_text = st.empty()

        translated_segments = []
        total_time = 0.0

        for i, segment in enumerate(segments):
            status_text.text(f"Translating segment {i + 1} / {total}...")
            result = translate_text(
                text=segment,
                source_lang=source_lang,
                target_lang=target_lang,
                auto_detect=auto,
            )

            if result.get("error"):
                translated_segments.append(f"[ERROR: {result['error']}]")
            else:
                translated_segments.append(result["translated_text"])
                total_time += result["translation_time"]

            progress_bar.progress((i + 1) / total)

        status_text.text("✅ Translation complete!")

        # Combine results
        full_translation = "\n\n".join(translated_segments)

        st.markdown("### 📝 Translated Document")
        st.info(f"**Time:** {format_time(total_time)} | "
                f"**Characters:** {format_number(len(full_translation))} | "
                f"**Words:** {format_number(len(full_translation.split()))}")

        st.text_area(
            "Translated content",
            value=full_translation,
            height=400,
            key="doc_result",
        )

        # Download
        st.download_button(
            "📥 Download Translated Document (.txt)",
            data=full_translation,
            file_name=f"bhashaai_{uploaded_file.name.rsplit('.', 1)[0]}_{target_lang.lower()}.txt",
            mime="text/plain",
            key="doc_download_btn",
        )
