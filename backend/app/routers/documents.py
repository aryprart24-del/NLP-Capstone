from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any
from ..services.document_service import document_service

router = APIRouter(prefix="/documents", tags=["Document Translation"])

@router.post("/upload")
async def upload_and_translate_document(
    file: UploadFile = File(...),
    source_lang: str = Form("auto"),
    target_lang: str = Form("hi")
):
    """
    Uploads and translates a file (.txt, .md, .json, .csv)
    while preserving structure and formatting.
    """
    try:
        content_bytes = await file.read()
        content_str = content_bytes.decode("utf-8", errors="replace")
        
        ext = file.filename.split('.')[-1] if '.' in file.filename else 'txt'

        result = document_service.translate_document(
            content=content_str,
            filename=file.filename,
            doc_format=ext,
            source_lang=source_lang,
            target_lang=target_lang
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
