import uuid
from datetime import datetime
from fastapi import APIRouter
from ..models.schemas import DialogueRequest, DialogueMessage
from ..services.translation_service import translation_service
from ..services.transliteration_service import get_transliteration

router = APIRouter(prefix="/dialogue", tags=["Bilingual Dialogue Assistant"])

@router.post("/message", response_model=DialogueMessage)
def send_dialogue_message(req: DialogueRequest):
    """
    Processes a real-time message in a bilingual dialogue session:
    Speaker A speaks speaker_a_lang -> Translated into speaker_b_lang.
    Speaker B speaks speaker_b_lang -> Translated into speaker_a_lang.
    """
    if req.speaker == "speaker_a":
        src_lang = req.speaker_a_lang
        tgt_lang = req.speaker_b_lang
    else:
        src_lang = req.speaker_b_lang
        tgt_lang = req.speaker_a_lang

    trans_res = translation_service.translate(
        text=req.text,
        source_lang=src_lang,
        target_lang=tgt_lang,
        include_back_translation=False
    )

    translated_text = trans_res["translated_text"]
    transliteration = get_transliteration(translated_text, tgt_lang)

    return DialogueMessage(
        id=str(uuid.uuid4())[:8],
        speaker=req.speaker,
        original_text=req.text,
        source_lang=src_lang,
        translated_text=translated_text,
        target_lang=tgt_lang,
        transliteration=transliteration,
        timestamp=datetime.now().strftime("%H:%M:%S")
    )
