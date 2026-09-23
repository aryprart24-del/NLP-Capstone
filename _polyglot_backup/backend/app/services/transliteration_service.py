"""
Transliteration Service
Provides phonetic transliteration between scripts (Devanagari <-> Latin/Romanized, Cyrillic, Pinyin, etc.)
Crucial for multilingual communication where users write languages phonetically.
"""
import re
from typing import Optional

# Devanagari to Latin phonetic mapping table (IAST / common Romanization)
DEVANAGARI_VOWELS = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ऋ': 'ri',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'अं': 'am', 'अः': 'ah'
}

DEVANAGARI_MATRAS = {
    'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'n', 'ँ': 'n', 'ः': 'h',
    '्': ''
}

DEVANAGARI_CONSONANTS = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
    'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
    'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gy', 'श्र': 'shr',
    'ड़': 'd', 'ढ़': 'dh', 'फ़': 'f', 'ज़': 'z', 'क़': 'q', 'ख़': 'kh', 'ग़': 'gh'
}

# Latin / Hinglish common phonetic patterns to Devanagari mappings
ROMAN_TO_DEVA_WORDS = {
    "namaste": "नमस्ते",
    "namaskar": "नमस्कार",
    "dhanyavad": "धन्यवाद",
    "shukriya": "शुक्रिया",
    "aap": "आप",
    "tum": "तुम",
    "main": "मैं",
    "mujhe": "मुझे",
    "hum": "हम",
    "kya": "क्या",
    "kyon": "क्यों",
    "kyun": "क्यों",
    "kaise": "कैसे",
    "kahan": "कहाँ",
    "kab": "कब",
    "kaun": "कौन",
    "haan": "हाँ",
    "nahi": "नहीं",
    "nahin": "नहीं",
    "theek": "ठीक",
    "kal": "कल",
    "aaj": "आज",
    "parso": "परसों",
    "college": "कॉलेज",
    "school": "स्कूल",
    "jaana": "जाना",
    "hai": "है",
    "hain": "हैं",
    "tha": "था",
    "thi": "थी",
    "the": "थे",
    "hoga": "होगा",
    "karna": "करना",
    "chahiye": "चाहिए",
    "accha": "अच्छा",
    "achha": "अच्छा",
    "bahut": "बहुत",
    "dost": "दोस्त",
    "ghar": "घर",
    "kaam": "काम",
    "paani": "पानी",
    "khana": "खाना",
    "samay": "समय",
    "pyaar": "प्यार",
    "madad": "मदद"
}

def devanagari_to_roman(text: str) -> str:
    """Converts Devanagari script to readable phonetic Latin characters."""
    result = []
    i = 0
    chars = list(text)
    n = len(chars)

    while i < n:
        char = chars[i]
        
        # Check vowels
        if char in DEVANAGARI_VOWELS:
            result.append(DEVANAGARI_VOWELS[char])
            i += 1
            continue

        # Check consonants
        if char in DEVANAGARI_CONSONANTS:
            consonant = DEVANAGARI_CONSONANTS[char]
            # Lookahead for matra or virama
            if i + 1 < n:
                next_char = chars[i + 1]
                if next_char == '्':  # Virama / halant: no vowel attached
                    result.append(consonant)
                    i += 2
                    continue
                elif next_char in DEVANAGARI_MATRAS:
                    result.append(consonant + DEVANAGARI_MATRAS[next_char])
                    i += 2
                    continue
            
            # If at the end of a word or before whitespace/punctuation, often inherent 'a' is suppressed in modern Hindi
            is_end_of_word = (i + 1 == n) or (chars[i + 1] in ' \t\n.,!?;:()[]{}""\'।')
            if is_end_of_word and len(result) > 0:
                result.append(consonant)
            else:
                result.append(consonant + 'a')
            i += 1
            continue

        # Matra standalone (unusual, but handle)
        if char in DEVANAGARI_MATRAS:
            result.append(DEVANAGARI_MATRAS[char])
            i += 1
            continue

        if char == '।':
            result.append('.')
            i += 1
            continue

        result.append(char)
        i += 1

    clean_res = ''.join(result)
    # Post-processing cleanup
    clean_res = re.sub(r'a([aeiou])', r'\1', clean_res)
    clean_res = re.sub(r'aa+', 'aa', clean_res)
    return clean_res

def roman_to_devanagari(text: str) -> str:
    """
    Converts Romanized Hindi / Hinglish to Devanagari script.
    Checks word-level dictionary first, then phonetic rules.
    """
    words = re.split(r'(\s+|[.,!?;:()।])', text)
    converted_tokens = []
    for token in words:
        lower_token = token.lower().strip()
        if lower_token in ROMAN_TO_DEVA_WORDS:
            converted_tokens.append(ROMAN_TO_DEVA_WORDS[lower_token])
        else:
            converted_tokens.append(token)
    return ''.join(converted_tokens)

def get_transliteration(text: str, lang_code: str) -> Optional[str]:
    """Generates phonetic transliteration for non-Latin script text."""
    if not text or not text.strip():
        return None

    # Detect if contains Devanagari characters
    has_devanagari = any('\u0900' <= char <= '\u097F' for char in text)
    if has_devanagari:
        return devanagari_to_roman(text)
    
    # If the text is Latin and language is indicated as Hindi/Marathi/etc., check Hinglish to Devanagari
    if lang_code in ['hi', 'mr', 'ne', 'sa'] and text.isascii():
        converted = roman_to_devanagari(text)
        if converted != text:
            return converted

    return None
