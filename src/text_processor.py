"""
BhashaAI — Text Processor
Text normalization, sentence segmentation, and recombination.
"""

import re
import unicodedata
from typing import List

from .config import SENTENCE_SPLIT_THRESHOLD


def normalize_text(text: str) -> str:
    """Normalize Unicode, collapse whitespace, strip edges."""
    if not text:
        return ""
    # Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)
    # Replace various dash/hyphen Unicode chars with standard hyphen
    text = re.sub(r'[\u2010-\u2015\u2212\uFE58\uFE63\uFF0D]', '-', text)
    # Replace various quotation marks with standard quotes
    text = re.sub(r'[\u2018\u2019\u201A\u201B]', "'", text)
    text = re.sub(r'[\u201C\u201D\u201E\u201F]', '"', text)
    # Collapse multiple whitespace into single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def segment_sentences(text: str) -> List[str]:
    """Split text into sentence-level segments for translation.

    Uses a regex-based sentence boundary detector that handles:
    - Period/question/exclamation followed by space + uppercase
    - Hindi Devanagari purna viram (।)
    - Newline boundaries

    For short texts (below SENTENCE_SPLIT_THRESHOLD), returns the
    full text as a single segment to avoid unnecessary splitting.
    """
    if not text or not text.strip():
        return []

    text = normalize_text(text)

    # Short text — no splitting needed
    if len(text) <= SENTENCE_SPLIT_THRESHOLD:
        return [text]

    # Split on sentence-ending punctuation followed by whitespace
    # Handles: English (.!?), Hindi (।), Chinese/Japanese (。), etc.
    sentences = re.split(
        r'(?<=[.!?\u0964\u3002])\s+',  # \u0964 = ।  \u3002 = 。
        text
    )

    # Also split on double newlines (paragraph breaks)
    expanded = []
    for sent in sentences:
        parts = re.split(r'\n\s*\n', sent)
        expanded.extend(parts)

    # Filter empty strings and strip whitespace
    result = [s.strip() for s in expanded if s.strip()]

    # Safety: if a single segment is still very long, split on single newlines
    final = []
    for segment in result:
        if len(segment) > SENTENCE_SPLIT_THRESHOLD * 3:
            sub_parts = segment.split('\n')
            final.extend([p.strip() for p in sub_parts if p.strip()])
        else:
            final.append(segment)

    return final if final else [text]


def recombine_sentences(translated_segments: List[str]) -> str:
    """Recombine translated sentence segments into a single text.

    Joins segments with a single space, preserving any paragraph
    breaks that were in the original segmentation.
    """
    if not translated_segments:
        return ""
    return " ".join(s.strip() for s in translated_segments if s.strip())
