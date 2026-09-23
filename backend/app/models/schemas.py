from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    script: Optional[str] = None
    family: Optional[str] = None

class DetectionRequest(BaseModel):
    text: str

class DetectionResponse(BaseModel):
    detected_code: str
    language_name: str
    confidence: float
    script: str
    is_code_switched: bool = False
    details: Optional[Dict[str, Any]] = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"
    tone: Optional[str] = "neutral"  # neutral, formal, casual, academic, diplomatic, simplified
    domain: Optional[str] = "general" # general, tech, medical, legal, business, tourism
    include_transliteration: bool = True
    include_linguistic_analysis: bool = True
    include_back_translation: bool = True
    api_key: Optional[str] = None

class TokenInfo(BaseModel):
    token: str
    pos: Optional[str] = None
    subwords: Optional[List[str]] = None
    index: int

class AttentionPair(BaseModel):
    source_token: str
    target_token: str
    weight: float

class LinguisticInsight(BaseModel):
    tokens: List[TokenInfo] = []
    complexity_score: float = 0.0
    sentiment: Optional[str] = "neutral"
    formality_detected: Optional[str] = "neutral"
    cultural_notes: List[str] = []
    grammar_notes: List[str] = []
    idioms_detected: List[Dict[str, str]] = []
    code_switched_segments: List[Dict[str, str]] = []

class TranslationResponse(BaseModel):
    source_text: str
    source_lang: str
    source_lang_name: str
    target_lang: str
    target_lang_name: str
    translated_text: str
    transliteration: Optional[str] = None
    source_transliteration: Optional[str] = None
    back_translation: Optional[str] = None
    fidelity_score: Optional[float] = None # 0.0 - 1.0 (semantic preservation score)
    linguistic_insights: Optional[LinguisticInsight] = None
    engine_used: str = "deep-translator (Google/MyMemory fallback)"

class PipelineStep(BaseModel):
    step_number: int
    name: str
    description: str
    input_data: Any
    output_data: Any
    metadata: Optional[Dict[str, Any]] = None

class PipelineInspectionRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "hi"

class PipelineInspectionResponse(BaseModel):
    source_text: str
    steps: List[PipelineStep]
    encoder_tokens: List[str]
    decoder_tokens: List[str]
    attention_matrix: List[List[float]] # source_len x target_len

class DialogueMessage(BaseModel):
    id: str
    speaker: str # 'speaker_a' or 'speaker_b'
    original_text: str
    source_lang: str
    translated_text: str
    target_lang: str
    transliteration: Optional[str] = None
    timestamp: str

class DialogueRequest(BaseModel):
    speaker: str
    text: str
    speaker_a_lang: str = "en"
    speaker_b_lang: str = "hi"

class PhrasebookItem(BaseModel):
    id: Optional[int] = None
    source_text: str
    source_lang: str
    translated_text: str
    target_lang: str
    category: Optional[str] = "General"
    notes: Optional[str] = None
    created_at: Optional[str] = None

class HistoryItem(BaseModel):
    id: Optional[int] = None
    source_text: str
    source_lang: str
    translated_text: str
    target_lang: str
    domain: Optional[str] = "general"
    tone: Optional[str] = "neutral"
    fidelity_score: Optional[float] = None
    created_at: Optional[str] = None

class DocumentTranslationRequest(BaseModel):
    filename: str
    content: str
    source_lang: str = "auto"
    target_lang: str = "hi"
    format: str = "txt" # txt, md, json, csv
