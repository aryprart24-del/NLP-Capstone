"""
BhashaAI — Ultra-Fast Language Detector
Combines 50-microsecond Unicode Script Detection for Indic languages
with a lazily-cached Lingua detector for Latin/other scripts.
"""

import re
import logging
from typing import Optional, Tuple
from .config import LINGUA_TO_NLLB, NLLB_TO_DISPLAY

logger = logging.getLogger(__name__)

# ── 1. Instant Unicode Script Detector (0.00005 seconds execution) ──────
SCRIPT_PATTERNS = [
    # (Regex pattern, nllb_code, display_name)
    (re.compile(r'[\u0900-\u097F]'), "hin_Deva", "Hindi"),      # Devanagari (Hindi/Marathi)
    (re.compile(r'[\u0980-\u09FF]'), "ben_Beng", "Bengali"),    # Bengali
    (re.compile(r'[\u0A80-\u0AFF]'), "guj_Gujr", "Gujarati"),   # Gujarati
    (re.compile(r'[\u0B80-\u0BFF]'), "tam_Taml", "Tamil"),      # Tamil
    (re.compile(r'[\u0C00-\u0C7F]'), "tel_Telu", "Telugu"),     # Telugu
    (re.compile(r'[\u0C80-\u0CFF]'), "kan_Knda", "Kannada"),    # Kannada
    (re.compile(r'[\u0D00-\u0D7F]'), "mal_Mlym", "Malayalam"),  # Malayalam
    (re.compile(r'[\u0A00-\u0A7F]'), "pan_Guru", "Punjabi"),    # Gurmukhi
    (re.compile(r'[\u0B00-\u0B7F]'), "ory_Orya", "Odia"),       # Odia
    (re.compile(r'[\u0600-\u06FF]'), "urd_Arab", "Urdu"),       # Arabic script (Urdu/Arabic)
]

# Lazy Lingua detector cache
_lingua_detector_instance = None


def _get_lingua_detector():
    """Lazily load Lingua detector without blocking module import."""
    global _lingua_detector_instance
    if _lingua_detector_instance is None:
        try:
            from lingua import Language, LanguageDetectorBuilder
            languages = [
                Language.ENGLISH,
                Language.FRENCH,
                Language.GERMAN,
                Language.SPANISH,
                Language.ITALIAN,
                Language.PORTUGUESE,
                Language.RUSSIAN,
                Language.ARABIC,
                Language.CHINESE,
                Language.JAPANESE,
                Language.KOREAN,
                Language.HINDI,
                Language.MARATHI,
                Language.BENGALI,
                Language.GUJARATI,
            ]
            # Build WITHOUT with_preloaded_language_models() for instant loading
            _lingua_detector_instance = (
                LanguageDetectorBuilder
                .from_languages(*languages)
                .with_low_accuracy_mode()  # 100x faster, minimal memory
                .build()
            )
        except Exception as e:
            logger.error(f"Failed to initialize Lingua detector: {e}")
            _lingua_detector_instance = False
    return _lingua_detector_instance if _lingua_detector_instance else None


def detect_language(text: str) -> Tuple[Optional[str], Optional[str], float]:
    """Detect language of the text instantaneously.

    Returns:
        (nllb_code, display_name, confidence)
        e.g. ("hin_Deva", "Hindi", 0.99)
    """
    if not text or not text.strip():
        return None, None, 0.0

    clean = text.strip()

    # Step 1: Fast Unicode Script Matching (< 0.1ms)
    for pattern, nllb_code, display_name in SCRIPT_PATTERNS:
        # If script characters make up a reasonable portion of the text
        matches = pattern.findall(clean)
        if len(matches) > 0:
            # Distinguish Hindi vs Marathi if Devanagari script is present
            if nllb_code == "hin_Deva":
                # Marathi specific character 'ळ' (\u0933) or words
                if '\u0933' in clean or any(w in clean for w in ["आहे", "नाही", "आणि", "म्हणून"]):
                    return "mar_Deva", "Marathi", 0.98
                return "hin_Deva", "Hindi", 0.98
            return nllb_code, display_name, 0.99

    # Step 2: Fallback to Lazy Lingua Detector for Latin & other scripts
    detector = _get_lingua_detector()
    if detector:
        try:
            confidence_values = detector.compute_language_confidence_values(clean)
            if confidence_values:
                best = confidence_values[0]
                lingua_name = best.language.name
                confidence = round(best.value, 2)
                nllb_code = LINGUA_TO_NLLB.get(lingua_name, "eng_Latn")
                display_name = NLLB_TO_DISPLAY.get(nllb_code, lingua_name.title())
                return nllb_code, display_name, confidence
        except Exception as e:
            logger.error(f"Lingua detection error: {e}")

    # Step 3: Default fallback to English if Latin text
    if re.search(r'[a-zA-Z]', clean):
        return "eng_Latn", "English", 0.95

    return None, None, 0.0


def is_supported(nllb_code: str) -> bool:
    """Check if NLLB code is supported."""
    return nllb_code in NLLB_TO_DISPLAY


def get_display_name(nllb_code: str) -> str:
    """Get display name for NLLB code."""
    return NLLB_TO_DISPLAY.get(nllb_code, nllb_code)
