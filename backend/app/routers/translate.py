from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.schemas import TranslationRequest, TranslationResponse, DetectionRequest, DetectionResponse, LanguageInfo
from ..services.translation_service import translation_service, detect_language, LANGUAGES_DB
from ..services.nlp_service import nlp_service
from ..services.storage_service import storage_service

router = APIRouter(prefix="/translate", tags=["Translation"])

@router.get("/languages", response_model=List[LanguageInfo])
def get_languages():
    """Returns list of supported languages with script and language family."""
    langs = []
    for code, info in LANGUAGES_DB.items():
        langs.append(LanguageInfo(
            code=code,
            name=info["name"],
            native_name=info["native"],
            script=info.get("script"),
            family=info.get("family")
        ))
    return langs

@router.post("/detect", response_model=DetectionResponse)
def detect(request: DetectionRequest):
    """Detects source language, script, and code-switching status."""
    res = detect_language(request.text)
    return DetectionResponse(
        detected_code=res["detected_code"],
        language_name=res["language_name"],
        confidence=res["confidence"],
        script=res["script"],
        is_code_switched=res.get("is_code_switched", False),
        details=res.get("details")
    )

@router.post("/", response_model=TranslationResponse)
def translate_text(req: TranslationRequest):
    """
    Translates input text with optional back-translation,
    transliteration, linguistic insights, and tone/domain adjustment.
    """
    try:
        result = translation_service.translate(
            text=req.text,
            source_lang=req.source_lang,
            target_lang=req.target_lang,
            tone=req.tone,
            domain=req.domain,
            include_back_translation=req.include_back_translation
        )

        insights = None
        if req.include_linguistic_analysis and result["translated_text"]:
            insights = nlp_service.analyze_linguistics(
                source_text=req.text,
                source_lang=result["source_lang"],
                target_lang=req.target_lang,
                translated_text=result["translated_text"]
            )

        # Record into history
        if result["translated_text"]:
            storage_service.add_history(
                source_text=req.text,
                source_lang=result["source_lang"],
                translated_text=result["translated_text"],
                target_lang=req.target_lang,
                domain=req.domain,
                tone=req.tone,
                fidelity_score=result["fidelity_score"] or 1.0
            )

        return TranslationResponse(
            source_text=result["source_text"],
            source_lang=result["source_lang"],
            source_lang_name=result["source_lang_name"],
            target_lang=result["target_lang"],
            target_lang_name=result["target_lang_name"],
            translated_text=result["translated_text"],
            transliteration=result["transliteration"],
            source_transliteration=result["source_transliteration"],
            back_translation=result["back_translation"],
            fidelity_score=result["fidelity_score"],
            linguistic_insights=insights,
            engine_used=result["engine_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
