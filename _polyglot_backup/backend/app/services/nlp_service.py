"""
NLP Linguistic & Pipeline Inspection Service
Implements subword tokenization, attention weight computation, grammar breakdown,
cultural nuance extraction, and the 6 multilingual challenges analysis from Aryan's presentation.
"""
import re
import math
from typing import List, Dict, Any, Optional
import httpx
from .transliteration_service import get_transliteration

# POS heuristic tagging dictionary for common English and Hindi words
POS_PATTERNS = [
    (r'\b(I|you|he|she|it|we|they|me|him|her|us|them|my|your|his|their|our)\b', 'PRON (Pronoun)'),
    (r'\b(मैं|मुझे|हम|आप|तुम|तू|वह|वे|मेरा|तुम्हारा|उसका|अपना)\b', 'PRON (सर्वनाम)'),
    (r'\b(am|is|are|was|were|be|been|being|have|has|had|do|does|did|go|going|gone|went|eat|play|read|write|see|say|come)\b', 'VERB (Verb)'),
    (r'\b(जाना|जा|रहा|रही|रहे|हूँ|है|हैं|था|थी|थे|होगा|कर|करना|बोलना|पढ़ना|लिखना|देखना)\b', 'VERB (क्रिया)'),
    (r'\b(college|school|book|water|food|house|car|computer|phone|language|friend|tomorrow|today|student|teacher)\b', 'NOUN (Noun)'),
    (r'\b(कॉलेज|स्कूल|किताब|पानी|खाना|घर|गाड़ी|कंप्यूटर|भाषा|दोस्त|कल|आज|छात्र|शिक्षक)\b', 'NOUN (संज्ञा)'),
    (r'\b(good|bad|big|small|happy|sad|beautiful|smart|fast|slow|multilingual|natural)\b', 'ADJ (Adjective)'),
    (r'\b(अच्छा|बुरा|बड़ा|छोटा|सुंदर|तेज़|धीमा|बहुभाषी|प्राकृतिक)\b', 'ADJ (विशेषण)'),
    (r'\b(to|in|on|at|by|for|with|about|against|between|into|through|during|before|after|above|below)\b', 'ADP (Preposition)'),
    (r'\b(में|पर|से|के|को|द्वारा|लिए|तथा|साथ)\b', 'ADP (परसर्ग / कारक)'),
    (r'\b(and|or|but|because|so|although|while)\b', 'CONJ (Conjunction)'),
    (r'\b(और|या|लेकिन|क्योंकि|इसलिए|परन्तु)\b', 'CONJ (योजक)')
]

def subword_tokenize(word: str) -> List[str]:
    """Simulates Byte-Pair Encoding (BPE) / WordPiece subword breakdown."""
    if len(word) <= 4:
        return [word]
    
    # Common prefixes / suffixes
    prefixes = ['multi', 'trans', 'pre', 'un', 're', 'in', 'dis', 'non']
    suffixes = ['ing', 'tion', 'sion', 'ment', 'able', 'ible', 'ness', 'ed', 'ly', 'er', 'est']
    
    lower = word.lower()
    for p in prefixes:
        if lower.startswith(p) and len(lower) > len(p) + 2:
            return [word[:len(p)], f"##{word[len(p):]}"]
            
    for s in suffixes:
        if lower.endswith(s) and len(lower) > len(s) + 2:
            split_idx = len(word) - len(s)
            return [word[:split_idx], f"##{word[split_idx:]}"]
            
    # Half-split fallback for long words
    if len(word) >= 8:
        mid = len(word) // 2
        return [word[:mid], f"##{word[mid:]}"]
        
    return [word]

def tag_pos(word: str) -> str:
    """Assigns part of speech tag using pattern matching and morphological cues."""
    clean = word.strip(".,!?;:()[]\"'।")
    for pattern, pos in POS_PATTERNS:
        if re.search(pattern, clean, re.IGNORECASE):
            return pos
            
    if clean.endswith(('tion', 'ment', 'ness', 'ity')):
        return "NOUN (Noun)"
    if clean.endswith(('ing', 'ed', 'ize', 'ify')):
        return "VERB (Verb)"
    if clean.endswith(('ly', 'ward')):
        return "ADV (Adverb)"
    if clean.endswith(('able', 'ful', 'ous', 'ive', 'al')):
        return "ADJ (Adjective)"
        
    return "WORD (General)"

def compute_attention_matrix(source_tokens: List[str], target_tokens: List[str]) -> List[List[float]]:
    """
    Computes a simulated Multi-Head Attention alignment matrix (Slide 6 Architecture).
    Produces higher attention weights for aligned semantic concepts and word position alignment.
    """
    if not source_tokens or not target_tokens:
        return []

    matrix = []
    src_len = len(source_tokens)
    tgt_len = len(target_tokens)

    for i, s_tok in enumerate(source_tokens):
        row = []
        s_norm = s_tok.lower().strip(".,!?;:()।")
        for j, t_tok in enumerate(target_tokens):
            t_norm = t_tok.lower().strip(".,!?;:()।")
            
            # Direct lexical / phonetic match
            if s_norm == t_norm and len(s_norm) > 1:
                weight = 0.95
            elif s_norm in ["college", "कॉलेज"] and t_norm in ["college", "कॉलेज"]:
                weight = 0.98
            elif s_norm in ["tomorrow", "कल"] and t_norm in ["tomorrow", "कल"]:
                weight = 0.96
            elif s_norm in ["go", "going", "जा", "जाना"] and t_norm in ["go", "going", "जा", "जाना", "रहा"]:
                weight = 0.92
            elif s_norm in ["i", "मैं", "मुझे"] and t_norm in ["i", "मैं", "मुझे"]:
                weight = 0.94
            else:
                # Position-based decay with soft dispersion (cross-attention Gaussian simulation)
                ideal_j = (i / max(1, src_len - 1)) * (tgt_len - 1) if src_len > 1 else 0
                dist = abs(j - ideal_j)
                weight = math.exp(-0.4 * (dist ** 2)) * 0.45 + 0.05

            row.append(round(weight, 3))
            
        # Softmax normalization across target tokens for this source token
        exp_row = [math.exp(w * 2.5) for w in row]
        sum_exp = sum(exp_row)
        norm_row = [round(v / sum_exp, 3) for v in exp_row]
        matrix.append(norm_row)

    return matrix

class NLPService:
    def analyze_linguistics(self, source_text: str, source_lang: str, target_lang: str, translated_text: str) -> Dict[str, Any]:
        """Provides in-depth linguistic and grammatical insights."""
        raw_tokens = re.findall(r'\b\w+\b|[.,!?;:()।]', source_text)
        token_infos = []

        for idx, t in enumerate(raw_tokens):
            subwords = subword_tokenize(t) if t.isalnum() else [t]
            pos = tag_pos(t) if t.isalnum() else "PUNCT (Punctuation)"
            token_infos.append({
                "token": t,
                "pos": pos,
                "subwords": subwords,
                "index": idx
            })

        # Cultural and grammatical nuances
        cultural_notes = []
        grammar_notes = []
        idioms_detected = []

        # Analyze Honorifics & Formality (Slide 7 Culture Challenge)
        if any(w in source_text for w in ["आप", "ji", "जी", "shree", "sir", "madam"]):
            cultural_notes.append("Formal honorific detected ('आप' / 'जी' / 'Sir'). Target language adapts to polite respectful registers.")
        elif any(w in source_text for w in ["तू", "yaar", "dude", "bro", "bhai"]):
            cultural_notes.append("Informal/colloquial familiarity detected ('तू' / 'yaar' / 'bro'). Recommended for peer conversation only.")

        # Grammar structural comparison (SVO vs SOV)
        if (source_lang == "en" and target_lang in ["hi", "mr", "ja", "ko"]) or (source_lang in ["hi", "mr", "ja", "ko"] and target_lang == "en"):
            grammar_notes.append(
                "Word-Order Transformation: Source uses Subject-Verb-Object (SVO) order in English, whereas Hindi/Marathi/Japanese use Subject-Object-Verb (SOV) order. The Transformer Decoder reorders constituents accordingly."
            )

        # Detect Idioms (Slide 7 Idioms Challenge)
        idiom_checks = {
            "piece of cake": "Idiom meaning 'very easy'. Translated contextually rather than literally ('आसान काम' vs 'केक का टुकड़ा').",
            "break a leg": "Theatrical idiom meaning 'good luck'. Contextual translation ensures meaning preservation.",
            "कल": "Hindi word 'कल' is context-dependent: it can mean 'yesterday' or 'tomorrow' depending on verb tense (जाना है / जाएगा = tomorrow; गया था = yesterday)."
        }
        for k, v in idiom_checks.items():
            if k.lower() in source_text.lower():
                idioms_detected.append({"idiom": k, "explanation": v})

        # Calculate complexity score
        words = [t for t in raw_tokens if t.isalnum()]
        avg_word_len = sum(len(w) for w in words) / max(1, len(words))
        complexity_score = min(1.0, round(avg_word_len / 10.0, 2))

        return {
            "tokens": token_infos,
            "complexity_score": complexity_score,
            "sentiment": "neutral",
            "formality_detected": "formal" if "आप" in source_text or "respect" in source_text else "neutral",
            "cultural_notes": cultural_notes,
            "grammar_notes": grammar_notes,
            "idioms_detected": idioms_detected,
            "code_switched_segments": []
        }

    def inspect_pipeline(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Simulates the entire 6-step multilingual translation pipeline from Slide 4 & Slide 6:
        1. Input
        2. Detect Source Language
        3. Encode (Tokens & Subword Embeddings)
        4. Translate (Transformer Encoder-Decoder & Attention)
        5. Decode (Target Language Generation)
        6. Output & Linguistic Assistance
        """
        from .translation_service import detect_language, translation_service

        # Step 1: Input
        s1_input = {"raw_text": text, "length": len(text)}

        # Step 2: Detect
        detection = detect_language(text)
        resolved_src = detection["detected_code"] if source_lang == "auto" else source_lang
        s2_detect = {
            "detected_code": detection["detected_code"],
            "language_name": detection["language_name"],
            "confidence": detection["confidence"],
            "script": detection["script"]
        }

        # Step 3: Encode
        raw_source_tokens = re.findall(r'\b\w+\b|[.,!?;:()।]', text)
        encoder_tokens = []
        token_embeddings = []
        for i, tok in enumerate(raw_source_tokens):
            sub = subword_tokenize(tok)
            encoder_tokens.extend(sub)
            # Simulated 4-dimensional embedding vector preview
            token_embeddings.append({
                "token": tok,
                "vector_sample": [round(math.sin(i + ord(c)) * 0.5, 3) for c in tok[:4].ljust(4, 'x')]
            })
        
        s3_encode = {
            "token_count": len(raw_source_tokens),
            "subword_tokens": encoder_tokens,
            "embeddings_preview": token_embeddings[:5]
        }

        # Step 4 & 5: Translate & Decode
        trans_res = translation_service.translate(
            text=text,
            source_lang=resolved_src,
            target_lang=target_lang,
            include_back_translation=True
        )
        translated_text = trans_res["translated_text"]
        raw_target_tokens = re.findall(r'\b\w+\b|[.,!?;:()।]', translated_text)
        decoder_tokens = []
        for tok in raw_target_tokens:
            decoder_tokens.extend(subword_tokenize(tok))

        attention_matrix = compute_attention_matrix(raw_source_tokens, raw_target_tokens)

        s4_translate = {
            "architecture": "Transformer (Multi-Head Self-Attention + Cross-Attention)",
            "layers": "6 Encoder Layers, 6 Decoder Layers",
            "attention_heads": 8,
            "engine_used": trans_res["engine_used"]
        }

        s5_decode = {
            "target_tokens": raw_target_tokens,
            "decoding_strategy": "Beam Search (Beam Width = 4)",
            "generated_text": translated_text
        }

        # Step 6: Output & Assistance
        linguistics = self.analyze_linguistics(text, resolved_src, target_lang, translated_text)
        s6_output = {
            "final_translation": translated_text,
            "transliteration": trans_res["transliteration"],
            "fidelity_score": trans_res["fidelity_score"],
            "back_translation": trans_res["back_translation"],
            "linguistic_assistance": linguistics
        }

        steps = [
            {
                "step_number": 1,
                "name": "Input Processing",
                "description": "Receives raw multi-modal input (text, speech transcript, or document content).",
                "input_data": text,
                "output_data": s1_input
            },
            {
                "step_number": 2,
                "name": "Language & Script Detection",
                "description": "Identifies Unicode codepoint script and classifies language via n-gram probabilities.",
                "input_data": text,
                "output_data": s2_detect
            },
            {
                "step_number": 3,
                "name": "Subword Tokenization & Embedding",
                "description": "Decomposes source sentence into subwords (Byte-Pair Encoding) and projects tokens to dense continuous vectors.",
                "input_data": s2_detect,
                "output_data": s3_encode
            },
            {
                "step_number": 4,
                "name": "Transformer Self-Attention & Cross-Attention",
                "description": "Applies multi-head attention to dynamically compute contextual relationships and weights across all tokens.",
                "input_data": s3_encode,
                "output_data": s4_translate
            },
            {
                "step_number": 5,
                "name": "Target Decoder Generation",
                "description": "Autoregressively decodes target language tokens using beam search decoding.",
                "input_data": s4_translate,
                "output_data": s5_decode
            },
            {
                "step_number": 6,
                "name": "Linguistic Assistance & Transliteration",
                "description": "Produces final meaning-preserving translation with grammar breakdown, transliteration, and back-translation fidelity.",
                "input_data": s5_decode,
                "output_data": s6_output
            }
        ]

        return {
            "source_text": text,
            "steps": steps,
            "encoder_tokens": raw_source_tokens,
            "decoder_tokens": raw_target_tokens,
            "attention_matrix": attention_matrix
        }

nlp_service = NLPService()
