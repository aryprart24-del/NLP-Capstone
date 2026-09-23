"""
BhashaAI — Core Translation Engine
NLLB-200 model loading, GPU inference, and translation pipeline.
"""

import logging
import time
from typing import List, Dict, Any, Optional

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from deep_translator import MyMemoryTranslator
from .config import (
    MODEL_NAME, get_device, get_device_info,
    SUPPORTED_LANGUAGES, NLLB_TO_DISPLAY, MYMEMORY_LANG_MAP,
    ENGINE_ONLINE, ENGINE_LOCAL,
    MAX_INPUT_LENGTH, BEAM_SIZE, MAX_NEW_TOKENS,
)

def translate_online(
    text: str,
    source_lang_name: str,
    target_lang_name: str,
) -> str:
    """Zero-download instant online translation using MyMemory / Google Translator."""
    src_str = MYMEMORY_LANG_MAP.get(source_lang_name, "english")
    tgt_str = MYMEMORY_LANG_MAP.get(target_lang_name, "hindi")
    translator = MyMemoryTranslator(source=src_str, target=tgt_str)
    return translator.translate(text)


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    auto_detect: bool = False,
    engine: str = ENGINE_ONLINE,
) -> Dict[str, Any]:
    """Full translation pipeline supporting Online Zero-Download and Local NLLB modes."""
    clean_text = normalize_text(text)
    if not clean_text:
        return _empty_result(text, source_lang, target_lang)

    # Resolve source language
    detected_name = None
    confidence = None
    if auto_detect or source_lang == "Auto Detect":
        nllb_code, detected_name, confidence = detect_language(clean_text)
        if nllb_code is None:
            return _error_result(text, source_lang, target_lang,
                                 "Could not detect source language. Please select manually.")
        src_nllb = nllb_code
        source_lang = detected_name or NLLB_TO_DISPLAY.get(nllb_code, source_lang)
    else:
        src_nllb = SUPPORTED_LANGUAGES.get(source_lang)

    tgt_nllb = SUPPORTED_LANGUAGES.get(target_lang)

    # Online Zero-Download Mode (Default)
    if engine.startswith("Online"):
        with timer() as t:
            try:
                translated_text = translate_online(clean_text, source_lang, target_lang)
                return {
                    "source_text": clean_text,
                    "translated_text": translated_text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "source_nllb": src_nllb,
                    "target_nllb": tgt_nllb,
                    "detected_lang": detected_name,
                    "confidence": confidence,
                    "translation_time": t.elapsed,
                    "word_count_source": len(clean_text.split()),
                    "word_count_target": len(translated_text.split()),
                    "char_count_source": len(clean_text),
                    "char_count_target": len(translated_text),
                    "engine_used": "Online (Instant)",
                    "error": None,
                }
            except Exception as e:
                logger.warning(f"Online translation failed: {e}. Falling back to local model.")

    # Local NLLB Offline Model Mode
    tokenizer, model, device, _ = load_model()

    if src_nllb is None:
        src_nllb = SUPPORTED_LANGUAGES.get(source_lang, "eng_Latn")
    if tgt_nllb is None:
        tgt_nllb = SUPPORTED_LANGUAGES.get(target_lang, "hin_Deva")

    if src_nllb == tgt_nllb:
        return {
            "source_text": clean_text,
            "translated_text": clean_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "source_nllb": src_nllb,
            "target_nllb": tgt_nllb,
            "detected_lang": detected_name,
            "confidence": confidence,
            "translation_time": 0.0,
            "word_count_source": len(clean_text.split()),
            "word_count_target": len(clean_text.split()),
            "char_count_source": len(clean_text),
            "char_count_target": len(clean_text),
            "engine_used": "Local (NLLB-200)",
            "error": None,
        }

    segments = segment_sentences(clean_text)
    translated_segments = []
    with timer() as t:
        for segment in segments:
            translated = _translate_segment(
                segment, src_nllb, tgt_nllb, tokenizer, model, device
            )
            translated_segments.append(translated)

    final_translation = recombine_sentences(translated_segments)

    return {
        "source_text": clean_text,
        "translated_text": final_translation,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_nllb": src_nllb,
        "target_nllb": tgt_nllb,
        "detected_lang": detected_name,
        "confidence": confidence,
        "translation_time": t.elapsed,
        "word_count_source": len(clean_text.split()),
        "word_count_target": len(final_translation.split()),
        "char_count_source": len(clean_text),
        "char_count_target": len(final_translation),
        "engine_used": "Local (NLLB-200)",
        "error": None,
    }
from .text_processor import normalize_text, segment_sentences, recombine_sentences
from .language_detector import detect_language
from .utils import timer

logger = logging.getLogger(__name__)

# ── Module-level model cache ──────────────────────────────────
_tokenizer = None
_model = None
_device = None
_model_load_time = None


import streamlit as st

@st.cache_resource(show_spinner=False)
def _cached_load_raw_model():
    """Load model once and cache across Streamlit reruns."""
    logger.info(f"Loading model into memory: {MODEL_NAME}")
    device = get_device()
    start_t = time.time()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model = model.to(device)
    model.eval()
    elapsed = time.time() - start_t
    logger.info(f"Model loaded on {device} in {elapsed:.2f}s")
    return tokenizer, model, device, elapsed


def load_model(force_reload: bool = False):
    """Load the NLLB-200 tokenizer and model onto the best device.

    Returns:
        (tokenizer, model, device, load_time_seconds)
    """
    global _tokenizer, _model, _device, _model_load_time

    if force_reload:
        _cached_load_raw_model.clear()

    tokenizer, model, device, elapsed = _cached_load_raw_model()
    _tokenizer = tokenizer
    _model = model
    _device = device
    _model_load_time = elapsed
    return tokenizer, model, device, elapsed


def get_model_status() -> Dict[str, Any]:
    """Return the current model/device status for UI display."""
    device_info = get_device_info()
    return {
        "model_name": MODEL_NAME,
        "model_loaded": _model is not None or "_cached_load_raw_model" in dir(),
        "model_load_time": f"{_model_load_time:.2f}s" if _model_load_time else "Cached",
        **device_info,
    }


def _translate_segment(
    text: str,
    src_nllb: str,
    tgt_nllb: str,
    tokenizer,
    model,
    device,
) -> str:
    """Translate a single text segment using NLLB-200.

    Returns:
        Translated text string.
    """
    tokenizer.src_lang = src_nllb

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=MAX_INPUT_LENGTH,
    ).to(device)

    tgt_lang_id = tokenizer.convert_tokens_to_ids(tgt_nllb)

    # Use inference_mode and use_cache for maximum speed
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tgt_lang_id,
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=BEAM_SIZE,
            use_cache=True,
            early_stopping=True,
        )

    translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translated[0] if translated else ""


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    auto_detect: bool = False,
) -> Dict[str, Any]:
    """Full translation pipeline for a single text input.

    Args:
        text: Source text to translate
        source_lang: Display name (e.g. "English") or "Auto Detect"
        target_lang: Display name (e.g. "Hindi")
        auto_detect: If True, detect the source language automatically

    Returns:
        Dict with keys:
            source_text, translated_text, source_lang, target_lang,
            source_nllb, target_nllb, detected_lang, confidence,
            translation_time, word_count_source, word_count_target,
            char_count_source, char_count_target
    """
    tokenizer, model, device, _ = load_model()

    # Normalize input
    clean_text = normalize_text(text)
    if not clean_text:
        return _empty_result(text, source_lang, target_lang)

    # Resolve source language
    detected_name = None
    confidence = None
    if auto_detect or source_lang == "Auto Detect":
        nllb_code, detected_name, confidence = detect_language(clean_text)
        if nllb_code is None:
            return _error_result(text, source_lang, target_lang,
                                 "Could not detect source language. Please select manually.")
        src_nllb = nllb_code
        source_lang = detected_name or NLLB_TO_DISPLAY.get(nllb_code, source_lang)
    else:
        src_nllb = SUPPORTED_LANGUAGES.get(source_lang)
        if src_nllb is None:
            return _error_result(text, source_lang, target_lang,
                                 f"Unsupported source language: {source_lang}")

    # Resolve target language
    tgt_nllb = SUPPORTED_LANGUAGES.get(target_lang)
    if tgt_nllb is None:
        return _error_result(text, source_lang, target_lang,
                             f"Unsupported target language: {target_lang}")

    # Same language check
    if src_nllb == tgt_nllb:
        return {
            "source_text": clean_text,
            "translated_text": clean_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "source_nllb": src_nllb,
            "target_nllb": tgt_nllb,
            "detected_lang": detected_name,
            "confidence": confidence,
            "translation_time": 0.0,
            "word_count_source": len(clean_text.split()),
            "word_count_target": len(clean_text.split()),
            "char_count_source": len(clean_text),
            "char_count_target": len(clean_text),
            "error": None,
        }

    # Segment long text
    segments = segment_sentences(clean_text)

    # Translate each segment
    translated_segments = []
    with timer() as t:
        for segment in segments:
            translated = _translate_segment(
                segment, src_nllb, tgt_nllb, tokenizer, model, device
            )
            translated_segments.append(translated)

    # Recombine
    final_translation = recombine_sentences(translated_segments)

    return {
        "source_text": clean_text,
        "translated_text": final_translation,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_nllb": src_nllb,
        "target_nllb": tgt_nllb,
        "detected_lang": detected_name,
        "confidence": confidence,
        "translation_time": t.elapsed,
        "word_count_source": len(clean_text.split()),
        "word_count_target": len(final_translation.split()),
        "char_count_source": len(clean_text),
        "char_count_target": len(final_translation),
        "error": None,
    }


def translate_batch(
    texts: List[str],
    source_lang: str,
    target_lang: str,
) -> List[Dict[str, Any]]:
    """Translate a list of texts. Used by the evaluation module."""
    results = []
    for text in texts:
        result = translate_text(text, source_lang, target_lang)
        results.append(result)
    return results


def _empty_result(text, source_lang, target_lang):
    return {
        "source_text": text,
        "translated_text": "",
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_nllb": None,
        "target_nllb": None,
        "detected_lang": None,
        "confidence": None,
        "translation_time": 0.0,
        "word_count_source": 0,
        "word_count_target": 0,
        "char_count_source": 0,
        "char_count_target": 0,
        "error": None,
    }


def _error_result(text, source_lang, target_lang, error_msg):
    result = _empty_result(text, source_lang, target_lang)
    result["error"] = error_msg
    return result
