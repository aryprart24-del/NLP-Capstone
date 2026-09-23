from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.schemas import HistoryItem, PhrasebookItem
from ..services.storage_service import storage_service

router = APIRouter(prefix="/history", tags=["History & Phrasebook"])

@router.get("/", response_model=List[HistoryItem])
def get_history(limit: int = 50):
    return storage_service.get_history(limit=limit)

@router.delete("/clear")
def clear_history():
    storage_service.clear_history()
    return {"status": "success", "message": "History cleared"}

@router.get("/phrasebook", response_model=List[PhrasebookItem])
def get_phrasebook(category: Optional[str] = None):
    return storage_service.get_phrasebook(category=category)

@router.post("/phrasebook", response_model=PhrasebookItem)
def add_phrase(item: PhrasebookItem):
    phrase_id = storage_service.add_phrase(
        source_text=item.source_text,
        source_lang=item.source_lang,
        translated_text=item.translated_text,
        target_lang=item.target_lang,
        category=item.category or "General",
        notes=item.notes or ""
    )
    item.id = phrase_id
    return item

@router.delete("/phrasebook/{phrase_id}")
def delete_phrase(phrase_id: int):
    storage_service.delete_phrase(phrase_id)
    return {"status": "success", "message": f"Phrase {phrase_id} deleted"}
