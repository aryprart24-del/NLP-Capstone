from fastapi import APIRouter
from ..models.schemas import PipelineInspectionRequest, PipelineInspectionResponse
from ..services.nlp_service import nlp_service

router = APIRouter(prefix="/pipeline", tags=["Pipeline Inspection"])

@router.post("/inspect", response_model=PipelineInspectionResponse)
def inspect_pipeline(req: PipelineInspectionRequest):
    """
    Simulates and visualizes the complete multilingual translation pipeline
    from the presentation (Input -> Detect -> Encode -> Translate/Attention -> Decode -> Output).
    """
    res = nlp_service.inspect_pipeline(
        text=req.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang
    )
    return PipelineInspectionResponse(
        source_text=res["source_text"],
        steps=res["steps"],
        encoder_tokens=res["encoder_tokens"],
        decoder_tokens=res["decoder_tokens"],
        attention_matrix=res["attention_matrix"]
    )
